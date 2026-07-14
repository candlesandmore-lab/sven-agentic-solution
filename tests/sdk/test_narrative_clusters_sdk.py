"""Interface tests for the narrative_clusters SDK surface (task_3), data-driven from
tests/fixtures/narrative_clusters/documents.yaml. Marked `live_endpoint`: calls the real
Anthropic API for the label node; skips when ANTHROPIC_API_KEY is not configured.
"""

from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    RawDocument,
    SourceType,
)
from technical_trader_solution.errors import InvalidClusterError, TechnicalTraderSolutionError
from technical_trader_solution.sdk import narrative_clusters as sdk

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/documents.yaml")


def test_get_cluster_trend_raises_invalid_cluster_error_for_unknown_id(tmp_path: Path) -> None:
    db_path = tmp_path / "narrative_clusters.sqlite"

    with pytest.raises(InvalidClusterError):
        sdk.get_cluster_trend("does-not-exist", db_path=db_path)


def test_technical_trader_solution_error_propagates_unchanged_from_sdk(tmp_path: Path) -> None:
    # The SDK layer never catches TechnicalTraderSolutionError itself (per the Domain
    # Exception Hierarchy section); confirm InvalidClusterError -- a subclass -- reaches
    # the caller as that exact type, not swallowed or wrapped.
    db_path = tmp_path / "narrative_clusters.sqlite"

    try:
        sdk.get_cluster_trend("does-not-exist", db_path=db_path)
    except TechnicalTraderSolutionError as exc:
        assert isinstance(exc, InvalidClusterError)
    else:
        pytest.fail("expected InvalidClusterError to propagate")


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
def test_sdk_run_and_read_back(tmp_path: Path) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not configured")

    documents = _load_documents()
    tickers = sorted({doc.ticker for doc in documents})
    db_path = tmp_path / "narrative_clusters.sqlite"

    def fixture_fetch_documents(ticker: str, since: datetime | None) -> list[RawDocument]:
        return [doc for doc in documents if doc.ticker == ticker]

    result = sdk.run_nightly_pipeline(
        tickers,
        run_date="2026-06-06",
        db_path=db_path,
        task_id="sdk-interface-test",
        fetch_documents=fixture_fetch_documents,
    )
    assert result["status"] == "succeeded", result

    clusters = sdk.get_clusters(date(2026, 6, 6), db_path=db_path)
    assert len(clusters) >= 1
    for cluster in clusters:
        dumped = cluster.model_dump(mode="json")
        assert "topic_embedding" not in dumped, "SDK must not expose the internal topic_embedding field"
        assert dumped["topic_label"]
        assert dumped["member_tickers"]

        trend = sdk.get_cluster_trend(cluster.cluster_id, db_path=db_path)
        assert len(trend) == 1
        assert "topic_embedding" not in trend[0]
