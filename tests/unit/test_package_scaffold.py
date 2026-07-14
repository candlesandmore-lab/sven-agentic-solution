"""Smoke tests for the technical_trader_solution package scaffold (story 001, task_1).

Capability-specific unit tests (extraction, clustering, trend computation) are added by
task_5_qa_validation once task_2's coded-agent pipeline exists.
"""

from __future__ import annotations


def test_package_imports() -> None:
    import technical_trader_solution
    import technical_trader_solution.core
    import technical_trader_solution.core.narrative_clusters
    import technical_trader_solution.sdk
    import technical_trader_solution.cli.main
    import technical_trader_solution.mcp.server

    assert technical_trader_solution.cli.main.app is not None
    assert technical_trader_solution.mcp.server.mcp is not None


def test_logging_configure_logger_writes_to_stderr_not_stdout(capsys, tmp_path) -> None:
    from technical_trader_solution.logging import configure_logger

    logger = configure_logger("technical_trader_solution.test", log_dir=tmp_path)
    logger.info("scaffold smoke test message")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "scaffold smoke test message" in captured.err
