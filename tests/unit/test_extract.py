"""Unit tests for the extract node (task_5), data-driven from
tests/fixtures/narrative_clusters/documents.yaml.

Deterministic and dependency-light (no embeddings, no model calls), unlike the live
end-to-end pipeline test -- these run without any API key configured.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.extract import (
    extract_narrative_finding,
    extract_narrative_findings,
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


def test_extract_narrative_findings_covers_every_document() -> None:
    documents = _load_documents()
    findings = extract_narrative_findings(documents)

    assert len(findings) == len(documents)
    for document, finding in zip(documents, findings):
        assert finding.ticker == document.ticker
        assert finding.source_type == document.source_type
        assert finding.source_id == document.source_id
        assert finding.published_at == document.published_at
        assert finding.keyphrases, f"expected keyphrases for {document.source_id}"
        assert finding.fetched_at is not None


@pytest.mark.parametrize(
    "ticker,expected_keyphrase_substring",
    [
        ("NVDA", "datacenter"),
        ("VST", "power"),
        ("IONQ", "quantum"),
        ("RGTI", "qubit"),
    ],
)
def test_extract_keyphrases_reflect_document_topic(
    ticker: str, expected_keyphrase_substring: str
) -> None:
    documents = [doc for doc in _load_documents() if doc.ticker == ticker]
    assert documents, f"fixture missing documents for {ticker}"

    for document in documents:
        finding = extract_narrative_finding(document)
        joined = " ".join(finding.keyphrases)
        assert expected_keyphrase_substring in joined, (
            f"expected a keyphrase containing {expected_keyphrase_substring!r} for "
            f"{document.source_id}, got {finding.keyphrases}"
        )


def test_extract_narrative_finding_is_empty_safe() -> None:
    document = RawDocument(
        ticker="ZZZZ",
        source_type=SourceType.NEWS,
        source_id="empty-doc",
        published_at=datetime(2026, 1, 1),
        text="",
    )
    finding = extract_narrative_finding(document)
    assert finding.keyphrases == []
    assert finding.entities == []
