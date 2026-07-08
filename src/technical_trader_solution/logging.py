"""Shared logging configuration for the Technical Trader Solution.

Never write informational, debug, warning, or status output via bare ``print()``. Never
stream logs to stdout: stdout is reserved for MCP stdio transport, and a bare stdout write
would corrupt that transport. Log to stderr and/or a log file only.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

DEFAULT_LOG_FILE = "technical_trader_solution.log"
DEFAULT_LOG_LEVEL = "INFO"


def configure_logger(
    name: str,
    *,
    log_file: str | Path | None = DEFAULT_LOG_FILE,
    log_level: str = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """Return a named logger writing to stderr and, when configured, a log file.

    Exposed identically across the CLI, SDK, and MCP surfaces so every caller can
    configure the same ``log_file`` and ``log_level`` knobs, per the interface-rules
    logging contract.
    """

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
