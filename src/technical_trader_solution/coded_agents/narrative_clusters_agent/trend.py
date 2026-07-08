"""Trend node: derive this run's trend snapshot for each cluster.

Per docs/implementation/01-narrative-cluster-discovery-surface.md's Data Contracts: the
trend snapshot retains each run's frequency_of_mention and company_breadth per cluster_id
for charting over time.
"""

from __future__ import annotations

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    ClusterRecord,
    ClusterTrendSnapshot,
)


def build_trend_snapshots(clusters: list[ClusterRecord]) -> list[ClusterTrendSnapshot]:
    return [
        ClusterTrendSnapshot(
            cluster_id=cluster.cluster_id,
            run_date=cluster.run_date,
            frequency_of_mention=cluster.frequency_of_mention,
            company_breadth=cluster.company_breadth,
        )
        for cluster in clusters
    ]
