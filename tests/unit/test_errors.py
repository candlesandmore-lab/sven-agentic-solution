"""Unit tests for the domain exception hierarchy and Unified Error Message Format
(story 002)."""

from __future__ import annotations

import logging

import pytest

from technical_trader_solution.errors import (
    ConfigurationError,
    DataProviderError,
    InvalidClusterError,
    TechnicalTraderSolutionError,
    format_error_message,
)


def test_domain_exceptions_subclass_the_base() -> None:
    assert issubclass(DataProviderError, TechnicalTraderSolutionError)
    assert issubclass(InvalidClusterError, TechnicalTraderSolutionError)
    assert issubclass(ConfigurationError, TechnicalTraderSolutionError)


def test_exception_construction_logs_class_name_and_message() -> None:
    logger = logging.getLogger("technical_trader_solution")
    captured: list[logging.LogRecord] = []
    handler = logging.Handler()
    handler.emit = captured.append
    logger.addHandler(handler)
    try:
        DataProviderError("FMP unreachable")
    finally:
        logger.removeHandler(handler)

    assert any(
        "DataProviderError" in record.getMessage() and "FMP unreachable" in record.getMessage()
        for record in captured
    )


def test_format_error_message_strips_error_suffix_and_masks(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMP_API_KEY", "secret-fmp-key")
    exc = DataProviderError("request failed with key secret-fmp-key")

    message = format_error_message(exc)

    assert message.startswith("DataProvider: ")
    assert "secret-fmp-key" not in message
    assert "***MASKED***" in message


def test_exception_message_not_masked_at_construction_time(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secret")

    exc = ConfigurationError("missing key sk-ant-secret")

    assert str(exc) == "missing key sk-ant-secret"
