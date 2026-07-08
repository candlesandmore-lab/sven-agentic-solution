from datetime import datetime, timezone

from sven_agentic_solution.narrative_cluster_workspace import (
    NarrativeClusterWorkspace,
    NarrativeFinding,
)


def test_build_clusters_groups_related_narrative_findings() -> None:
    workspace = NarrativeClusterWorkspace()
    workspace.ingest_finding(
        NarrativeFinding(
            source_type="news",
            source_id="n-1",
            ticker="AAPL",
            storyline="ai infrastructure",
            topic="data center buildout",
            evidence_excerpt="AAPL mentioned in new data center buildout",
            mention_timestamp=datetime(2026, 7, 1, tzinfo=timezone.utc),
            confidence=0.9,
        )
    )
    workspace.ingest_finding(
        NarrativeFinding(
            source_type="earnings",
            source_id="e-1",
            ticker="MSFT",
            storyline="AI infrastructure",
            topic="data center buildout",
            evidence_excerpt="MSFT discussed data center expansion",
            mention_timestamp=datetime(2026, 7, 2, tzinfo=timezone.utc),
            confidence=0.8,
        )
    )

    clusters = workspace.build_clusters()

    assert len(clusters) == 1
    assert clusters[0].storyline == "Ai Infrastructure"
    assert clusters[0].topic_summary == "Data Center Buildout"
    assert clusters[0].member_tickers == ["AAPL", "MSFT"]
    assert clusters[0].trend_metrics["mention_count"] == 2
    assert clusters[0].trend_metrics["company_breadth"] == 2
