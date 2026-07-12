"""Interface test for the fetch node's FMPClient (task_5), reusing
tests/fixtures/narrative_clusters/documents.yaml's tickers as live FMP input when
FMP_API_KEY is configured. Skips (not fails) otherwise, per the fixture/credential-skip
convention -- the CLI/SDK/MCP interface tests already cover the mocked path via each
test's own `fixture_fetch_documents` callable, which stands in for FMPClient regardless
of whether FMP_API_KEY is set.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.fetch import FMPClient
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import RawDocument

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/documents.yaml")


def _fixture_tickers() -> list[str]:
    if not FIXTURE_PATH.exists():
        pytest.skip(f"required fixture missing: {FIXTURE_PATH}")
    raw = yaml.safe_load(FIXTURE_PATH.read_text())
    return sorted({entry["ticker"] for entry in raw["documents"]})


@pytest.mark.live_endpoint
def test_fmp_client_fetch_documents_live() -> None:
    if not os.environ.get("FMP_API_KEY"):
        pytest.skip("FMP_API_KEY not configured")

    client = FMPClient()
    ticker = _fixture_tickers()[0]
    documents = client.fetch_documents(ticker)

    assert isinstance(documents, list)
    for document in documents:
        assert isinstance(document, RawDocument)
        assert document.ticker == ticker
