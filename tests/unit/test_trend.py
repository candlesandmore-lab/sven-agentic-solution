"""Unit tests for the trend node (task_5), data-driven from
tests/fixtures/narrative_clusters/prior_run_clusters.yaml.

Deterministic: no clustering, embeddings, or model calls -- runs without any API key.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import ClusterRecord
from technical_trader_solution.coded_agents.narrative_clusters_agent.trend import (
    build_trend_snapshots,
)

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/prior_run_clusters.yaml")


def _load_clusters() -> list[ClusterRecord]:
    if not FIXTURE_PATH.exists():
        pytest.skip(f"required fixture missing: {FIXTURE_PATH}")
    fixture = yaml.safe_load(FIXTURE_PATH.read_text())
    return [ClusterRecord(**entry) for entry in fixture["prior_clusters"]]


def test_build_trend_snapshots_maps_every_cluster() -> None:
    clusters = _load_clusters()
    snapshots = build_trend_snapshots(clusters)

    assert len(snapshots) == len(clusters)
    for cluster, snapshot in zip(clusters, snapshots):
        assert snapshot.cluster_id == cluster.cluster_id
        assert snapshot.run_date == cluster.run_date
        assert snapshot.frequency_of_mention == cluster.frequency_of_mention
        assert snapshot.company_breadth == cluster.company_breadth


def test_build_trend_snapshots_excludes_internal_fields() -> None:
    clusters = _load_clusters()
    snapshots = build_trend_snapshots(clusters)

    for snapshot in snapshots:
        dumped = snapshot.model_dump()
        assert "topic_embedding" not in dumped
        assert "topic_label" not in dumped
        assert "member_tickers" not in dumped


def test_build_trend_snapshots_empty_input() -> None:
    assert build_trend_snapshots([]) == []
