"""Domain exception hierarchy for the Technical Trader Solution (story 002).

Every subclass logs its own class name and message to the shared logger at construction
time, so the error condition is captured even when a calling layer swallows or transforms
the exception before it reaches a handler. Each subclass's message carries literal values;
masking is applied once, at Unified Error Message Format assembly time via
`format_error_message`, not at construction time here, so a message is never double-masked.

Per docs/implementation/02-logging-and-error-handling.md's Domain Exception Hierarchy
section: the SDK layer never catches these; the CLI layer catches them at the command
boundary and exits non-zero; the MCP layer catches them at the tool boundary and returns
the unified message in the tool's own response; the dashboard catches them around each SDK
call and renders the unified message in an `st.error(...)` banner.
"""

from __future__ import annotations

import logging

_logger = logging.getLogger("technical_trader_solution")


class TechnicalTraderSolutionError(Exception):
    """Base for every domain exception raised by the Technical Trader Solution's core."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        _logger.error("%s: %s", type(self).__name__, message)


class DataProviderError(TechnicalTraderSolutionError):
    """The FMP data provider is unreachable or returned an unexpected response."""


class InvalidClusterError(TechnicalTraderSolutionError):
    """A requested `cluster_id` does not exist."""


class ConfigurationError(TechnicalTraderSolutionError):
    """A required setting (for example `FMP_API_KEY`) is missing or invalid."""


def format_error_message(exc: TechnicalTraderSolutionError) -> str:
    """The Unified Error Message Format: `"{error_type}: {message}"`, masked once here."""

    from technical_trader_solution.logging import mask_sensitive

    error_type = type(exc).__name__.removesuffix("Error")
    return mask_sensitive(f"{error_type}: {exc}")
