"""Interface tests for the `tts narrative` CLI commands (task_3), data-driven from
tests/fixtures/narrative_clusters/documents.yaml. Marked `live_endpoint`: calls the real
Anthropic API for the label node; skips when ANTHROPIC_API_KEY is not configured.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

import technical_trader_solution.cli.narrative_clusters as cli_mod
from technical_trader_solution.cli.main import app
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    RawDocument,
    SourceType,
)
from technical_trader_solution.sdk import narrative_clusters as sdk

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/documents.yaml")


def test_cli_show_trend_unknown_cluster_exits_nonzero_with_unified_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_path = tmp_path / "narrative_clusters.sqlite"
    monkeypatch.setattr(
        cli_mod, "get_cluster_trend", lambda cluster_id: sdk.get_cluster_trend(cluster_id, db_path=db_path)
    )

    runner = CliRunner()
    result = runner.invoke(app, ["narrative", "show-trend", "does-not-exist"])

    assert result.exit_code == 1
    assert "InvalidCluster:" in result.output
    assert "Traceback" not in result.output


def _load_documents() -> list[RawDocument]:
    if not FIXTURE_PATH.exists():
        pytest.skip(f"required fixture missing: {FIXTURE_PATH}")
    raw = yaml.safe_load(FIXTURE_PATH.read_text())
    return [
        RawDocument(
            ticker=entry["ticker"],
            source_type=SourceType(entry["source_type"]),
            source_id=entry["source_id"],
            published_at=datetime.fromisoformat(entry["published_at"]),
            text=entry["text"],
        )
        for entry in raw["documents"]
    ]


@pytest.mark.live_endpoint
def test_cli_run_nightly_and_show_clusters(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not configured")

    documents = _load_documents()
    tickers = sorted({doc.ticker for doc in documents})
    db_path = tmp_path / "narrative_clusters.sqlite"

    def fixture_fetch_documents(ticker: str, since: datetime | None) -> list[RawDocument]:
        return [doc for doc in documents if doc.ticker == ticker]

    def patched_run_nightly_pipeline(tickers, run_date=None, **_ignored):
        return sdk.run_nightly_pipeline(
            tickers,
            run_date=run_date,
            db_path=db_path,
            task_id="cli-interface-test",
            fetch_documents=fixture_fetch_documents,
        )

    monkeypatch.setattr(cli_mod, "run_nightly_pipeline", patched_run_nightly_pipeline)
    monkeypatch.setattr(cli_mod, "get_clusters", lambda run_date=None: sdk.get_clusters(run_date, db_path=db_path))
    monkeypatch.setattr(
        cli_mod, "get_cluster_trend", lambda cluster_id: sdk.get_cluster_trend(cluster_id, db_path=db_path)
    )

    runner = CliRunner()
    args = ["narrative", "run-nightly", "--run-date", "2026-06-06"]
    for ticker in tickers:
        args += ["--ticker", ticker]
    result = runner.invoke(app, args)

    assert result.exit_code == 0, result.output
    assert "cluster(s) found" in result.output
    assert "topic_embedding" not in result.output

    result = runner.invoke(app, ["narrative", "show-clusters", "--run-date", "2026-06-06"])
    assert result.exit_code == 0, result.output
    assert "topic_embedding" not in result.output
    assert "cluster_id" in result.output
