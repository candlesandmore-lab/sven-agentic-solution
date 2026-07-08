from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class NarrativeFinding:
    source_type: str
    source_id: str
    ticker: str
    storyline: str
    topic: str
    evidence_excerpt: str
    mention_timestamp: datetime
    confidence: float = 0.0


@dataclass(slots=True)
class NarrativeCluster:
    cluster_id: str
    storyline: str
    topic_summary: str
    member_tickers: list[str] = field(default_factory=list)
    trend_metrics: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class NarrativeClusterWorkspace:
    """Stateful workspace for narrative-cluster discovery."""

    def __init__(self) -> None:
        self._findings: list[NarrativeFinding] = []
        self._clusters: list[NarrativeCluster] = []

    def ingest_finding(self, finding: NarrativeFinding) -> None:
        self._findings.append(finding)

    def build_clusters(self) -> list[NarrativeCluster]:
        grouped: dict[tuple[str, str], list[NarrativeFinding]] = {}
        for finding in self._findings:
            key = (finding.storyline.lower().strip(), finding.topic.lower().strip())
            grouped.setdefault(key, []).append(finding)

        clusters: list[NarrativeCluster] = []
        for (storyline, topic), findings in sorted(grouped.items()):
            tickers = sorted({finding.ticker for finding in findings})
            cluster = NarrativeCluster(
                cluster_id=f"cluster-{len(clusters) + 1}",
                storyline=storyline.title(),
                topic_summary=topic.title(),
                member_tickers=tickers,
                trend_metrics={
                    "mention_count": len(findings),
                    "company_breadth": len(tickers),
                },
            )
            clusters.append(cluster)

        self._clusters = clusters
        return clusters

    def get_clusters(self) -> list[NarrativeCluster]:
        return list(self._clusters)
