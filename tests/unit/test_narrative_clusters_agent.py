"""End-to-end test for the Narrative Extraction and Clustering Pipeline coded agent
(task_2), data-driven from tests/fixtures/narrative_clusters/documents.yaml.

Marked `live_endpoint`: it calls the real Anthropic API for the label node and downloads
the sentence-transformer embedding model on first run. Skips (not fails) when
ANTHROPIC_API_KEY is not configured, per the fixture/credential-skip convention.
"""

from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.agent import (
    NarrativeClustersAgent,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    RawDocument,
    SourceType,
)

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/documents.yaml")


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
def test_narrative_clusters_agent_end_to_end(tmp_path: Path) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not configured")

    documents = _load_documents()
    tickers = sorted({doc.ticker for doc in documents})

    def fixture_fetch_documents(ticker: str, since: datetime | None) -> list[RawDocument]:
        return [doc for doc in documents if doc.ticker == ticker]

    agent = NarrativeClustersAgent(
        db_path=tmp_path / "narrative_clusters.sqlite",
        state_db_path=tmp_path / "narrative-clusters-agent-state.sqlite",
        log_file=tmp_path / "narrative-clusters-agent.log",
    )

    result = agent.run(
        task_id="test-run-2026-06-06",
        inputs={
            "run_date": "2026-06-06",
            "tickers": tickers,
            "fetch_documents": fixture_fetch_documents,
        },
    )

    assert result["status"] == "succeeded", result
    output = result["output"]
    assert output["documents_fetched"] == len(documents)
    assert output["findings_count"] == len(documents)

    clusters = output["clusters"]
    assert len(clusters) >= 1, "expected at least one multi-ticker cluster from the two-topic fixture"

    for cluster in clusters:
        assert len(cluster["member_tickers"]) >= 2
        assert cluster["topic_label"]
        assert cluster["frequency_of_mention"] > 0
        assert cluster["company_breadth"] == len(cluster["member_tickers"])

    # Trend snapshots and clusters are queryable back out of the store for this run.
    stored_clusters = agent.store.get_clusters(run_date=date(2026, 6, 6))
    assert len(stored_clusters) == len(clusters)
    for cluster in stored_clusters:
        trend = agent.store.get_cluster_trend(cluster.cluster_id)
        assert len(trend) == 1
        assert trend[0].frequency_of_mention == cluster.frequency_of_mention
