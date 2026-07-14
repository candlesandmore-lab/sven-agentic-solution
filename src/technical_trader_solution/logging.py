"""Shared logging configuration for the Technical Trader Solution.

Never write informational, debug, warning, or status output via bare ``print()``. Never
stream logs to stdout: stdout is reserved for MCP stdio transport, and a bare stdout write
would corrupt that transport. Log to stderr and/or a log file only.

See docs/implementation/02-logging-and-error-handling.md for the full contract: run-timestamp
coordination across nested processes, the masked-fields allowlist, and third-party logger
redirection.
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from technical_trader_solution.errors import ConfigurationError

PACKAGE_NAME = "technical_trader_solution"
DEFAULT_LOG_DIR = Path(PACKAGE_NAME)
DEFAULT_LOG_LEVEL = "info"
RUN_TIMESTAMP_ENV_VAR = "TTS_RUN_TIMESTAMP"
VALID_LOG_LEVELS = ("info", "debug", "warning", "error")

# Known secret environment-variable names, masked wherever their configured value would
# otherwise appear in a log record or error message. Extend this tuple -- not a broad
# os.environ pattern scan -- when a new secret is introduced, so an unrelated third-party
# environment variable is never masked by accident.
MASKED_ENV_VARS = ("FMP_API_KEY", "ANTHROPIC_API_KEY")

# Third-party loggers that log external API traffic through Python's logging module and
# have no handler of their own, redirected into the shared log file wherever configure_logger
# runs, since they would otherwise only reach the root logger's default, unmasked,
# terminal-only last-resort handler.
THIRD_PARTY_LOGGER_NAMES = ("httpx", "httpcore")

_root_configured = False


def resolve_run_timestamp() -> str:
    """Resolve one run timestamp per process tree.

    Reuses ``TTS_RUN_TIMESTAMP`` from the environment when already set (by a parent
    process, or an earlier call in this process); otherwise generates one and writes it
    back, so every process in the tree -- including a subprocess this run shells out to --
    resolves to the same log filename regardless of subprocess startup timing.
    """

    existing = os.environ.get(RUN_TIMESTAMP_ENV_VAR)
    if existing:
        return existing
    generated = datetime.now().strftime("%Y%m%dT%H%M%S")
    os.environ[RUN_TIMESTAMP_ENV_VAR] = generated
    return generated


def mask_sensitive(text: str) -> str:
    """Replace any configured secret value from `MASKED_ENV_VARS` found in `text`.

    Re-reads `os.environ` on every call, so a value set or changed after import is still
    covered.
    """

    masked = text
    for name in MASKED_ENV_VARS:
        value = os.environ.get(name)
        if value:
            masked = masked.replace(value, "***MASKED***")
    return masked


class MaskingFilter(logging.Filter):
    """Renders each record's message once, masking any configured secret value.

    Attached to handlers, not to a `Logger` object: a `Filter` on a `Logger` only applies
    to records that logger itself emits, not to records a child logger propagates past it,
    which would miss third-party library output.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = mask_sensitive(record.getMessage())
        record.args = None
        return True


def configure_logger(
    name: str,
    *,
    log_dir: str | Path | None = None,
    log_level: str = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """Return a named logger writing to stderr and a shared, datetime-stamped log file.

    Exposed identically across the CLI, SDK, and MCP surfaces so every caller can
    configure the same ``log_dir``/``log_level`` knobs. `log_dir` -- whether the default
    or a caller-supplied path -- is created if it does not already exist. The first call
    in a process also mirrors its masked handlers onto the root logger and redirects
    `THIRD_PARTY_LOGGER_NAMES` into the same shared log file, so any library that logs
    without its own handler is captured and masked too. A subsequent call for a
    different `name` reuses the run timestamp and root-logger configuration already
    resolved by the first call.
    """

    global _root_configured

    normalized_level = log_level.strip().lower()
    if normalized_level not in VALID_LOG_LEVELS:
        raise ConfigurationError(
            f"log_level must be one of {VALID_LOG_LEVELS}, got {log_level!r}."
        )

    resolved_dir = Path(log_dir) if log_dir is not None else DEFAULT_LOG_DIR
    resolved_dir.mkdir(parents=True, exist_ok=True)
    timestamp = resolve_run_timestamp()
    log_file = resolved_dir / f"{PACKAGE_NAME}_{timestamp}.log"

    logger = logging.getLogger(name)
    logger.setLevel(normalized_level.upper())
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    masking_filter = MaskingFilter()

    if not logger.handlers:
        stderr_handler = logging.StreamHandler(stream=sys.stderr)
        stderr_handler.setFormatter(formatter)
        stderr_handler.addFilter(masking_filter)
        logger.addHandler(stderr_handler)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(masking_filter)
        logger.addHandler(file_handler)

    if not _root_configured:
        root_logger = logging.getLogger()

        root_stderr_handler = logging.StreamHandler(stream=sys.stderr)
        root_stderr_handler.setFormatter(formatter)
        root_stderr_handler.addFilter(masking_filter)
        root_logger.addHandler(root_stderr_handler)

        root_file_handler = logging.FileHandler(log_file)
        root_file_handler.setFormatter(formatter)
        root_file_handler.addFilter(masking_filter)
        root_logger.addHandler(root_file_handler)
        root_logger.setLevel(normalized_level.upper())

        for third_party_name in THIRD_PARTY_LOGGER_NAMES:
            third_party_logger = logging.getLogger(third_party_name)
            third_party_logger.handlers.clear()
            third_party_logger.addHandler(root_stderr_handler)
            third_party_logger.addHandler(root_file_handler)
            third_party_logger.propagate = False

        _root_configured = True

    return logger
