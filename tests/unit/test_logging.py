"""Unit tests for shared logging configuration (story 002): sensitive-data masking,
run-timestamp coordination across nested processes, and third-party logger redirection.
"""

from __future__ import annotations

import logging

import pytest

from technical_trader_solution import logging as tts_logging
from technical_trader_solution.errors import ConfigurationError


@pytest.fixture(autouse=True)
def _reset_logging_state(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(tts_logging.RUN_TIMESTAMP_ENV_VAR, raising=False)
    monkeypatch.setattr(tts_logging, "_root_configured", False)
    yield
    for name in tts_logging.THIRD_PARTY_LOGGER_NAMES:
        third_party_logger = logging.getLogger(name)
        third_party_logger.handlers.clear()
        third_party_logger.propagate = True
    logging.getLogger().handlers.clear()


def test_mask_sensitive_replaces_configured_secret_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FMP_API_KEY", "secret-fmp-key")
    text = "request failed with apikey=secret-fmp-key in the URL"

    masked = tts_logging.mask_sensitive(text)

    assert "secret-fmp-key" not in masked
    assert "***MASKED***" in masked


def test_mask_sensitive_leaves_unrelated_text_unchanged(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FMP_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    text = "nothing sensitive here"

    assert tts_logging.mask_sensitive(text) == text


def test_masking_filter_masks_log_record_message(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-secret")
    logger = tts_logging.configure_logger("test.masking.handler", log_dir=tmp_path)

    logger.error("auth failed with key sk-ant-secret")

    log_file = next(tmp_path.glob("*.log"))
    contents = log_file.read_text()
    assert "sk-ant-secret" not in contents
    assert "***MASKED***" in contents


def test_configure_logger_creates_default_and_caller_supplied_log_dir(tmp_path) -> None:
    custom_dir = tmp_path / "nested" / "log-dir"
    assert not custom_dir.exists()

    tts_logging.configure_logger("test.logdir.creation", log_dir=custom_dir)

    assert custom_dir.is_dir()


def test_configure_logger_filename_uses_run_timestamp(tmp_path) -> None:
    tts_logging.configure_logger("test.filename.timestamp", log_dir=tmp_path)

    timestamp = tts_logging.resolve_run_timestamp()
    expected = tmp_path / f"technical_trader_solution_{timestamp}.log"
    assert expected.exists()


def test_configure_logger_rejects_invalid_log_level(tmp_path) -> None:
    with pytest.raises(ConfigurationError):
        tts_logging.configure_logger("test.invalid.level", log_dir=tmp_path, log_level="verbose")


def test_resolve_run_timestamp_reused_when_already_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(tts_logging.RUN_TIMESTAMP_ENV_VAR, "20260101T000000")

    assert tts_logging.resolve_run_timestamp() == "20260101T000000"


def test_resolve_run_timestamp_generated_once_and_reused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(tts_logging.RUN_TIMESTAMP_ENV_VAR, raising=False)

    first = tts_logging.resolve_run_timestamp()
    second = tts_logging.resolve_run_timestamp()

    assert first == second


def test_configure_logger_mirrors_masked_handlers_onto_root_logger(tmp_path) -> None:
    tts_logging.configure_logger("test.root.mirroring", log_dir=tmp_path)

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) >= 2


def test_third_party_logger_without_own_handler_is_captured_and_masked(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setenv("FMP_API_KEY", "secret-fmp-key")
    tts_logging.configure_logger("test.third.party", log_dir=tmp_path)
    log_file = next(tmp_path.glob("*.log"))

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.error("GET request failed apikey=secret-fmp-key")

    contents = log_file.read_text()
    assert "GET request failed" in contents
    assert "secret-fmp-key" not in contents
