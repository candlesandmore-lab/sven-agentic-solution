"""Interface tests for the narrative_clusters MCP tools (task_3), data-driven from
tests/fixtures/narrative_clusters/documents.yaml. Marked `live_endpoint`: calls the real
Anthropic API for the label node; skips when ANTHROPIC_API_KEY is not configured.
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    RawDocument,
    SourceType,
)
from technical_trader_solution.mcp.server import mcp
from technical_trader_solution.sdk import narrative_clusters as sdk

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


def test_mcp_tools_registered() -> None:
    tool_names = {tool.name for tool in asyncio.run(mcp.list_tools())}
    assert {
        "narrative_run_nightly_pipeline",
        "narrative_get_clusters",
        "narrative_get_cluster_trend",
    } <= tool_names


def test_mcp_get_cluster_trend_returns_unified_error_for_unknown_cluster(tmp_path: Path) -> None:
    import technical_trader_solution.mcp.narrative_clusters as mcp_mod

    db_path = tmp_path / "narrative_clusters.sqlite"
    original_get_cluster_trend = mcp_mod.get_cluster_trend
    mcp_mod.get_cluster_trend = lambda cluster_id: original_get_cluster_trend(cluster_id, db_path=db_path)
    try:
        tool_result = asyncio.run(
            mcp.call_tool("narrative_get_cluster_trend", {"request": {"cluster_id": "does-not-exist"}})
        )
    finally:
        mcp_mod.get_cluster_trend = original_get_cluster_trend

    payload = tool_result.structured_content["result"] if tool_result.structured_content else tool_result.data
    assert "error" in payload
    assert payload["error"].startswith("InvalidCluster:")


@pytest.mark.live_endpoint
def test_mcp_get_clusters_excludes_topic_embedding(tmp_path: Path) -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not configured")

    documents = _load_documents()
    tickers = sorted({doc.ticker for doc in documents})
    db_path = tmp_path / "narrative_clusters.sqlite"

    def fixture_fetch_documents(ticker: str, since: datetime | None) -> list[RawDocument]:
        return [doc for doc in documents if doc.ticker == ticker]

    # Populate the store directly through the SDK (same path the coded agent itself
    # uses); the MCP tool call below then exercises the read path end to end.
    result = sdk.run_nightly_pipeline(
        tickers,
        run_date="2026-06-06",
        db_path=db_path,
        task_id="mcp-interface-test",
        fetch_documents=fixture_fetch_documents,
    )
    assert result["status"] == "succeeded", result

    import technical_trader_solution.mcp.narrative_clusters as mcp_mod

    original_get_clusters = mcp_mod.get_clusters
    mcp_mod.get_clusters = lambda run_date=None: original_get_clusters(run_date, db_path=db_path)
    try:
        tool_result = asyncio.run(
            mcp.call_tool("narrative_get_clusters", {"request": {"run_date": "2026-06-06"}})
        )
    finally:
        mcp_mod.get_clusters = original_get_clusters

    clusters = tool_result.structured_content["result"] if tool_result.structured_content else tool_result.data
    assert len(clusters) >= 1
    for cluster in clusters:
        assert "topic_embedding" not in cluster
        assert cluster["topic_label"]
