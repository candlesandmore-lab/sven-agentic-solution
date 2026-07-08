"""Unit tests for the cluster-identity matching algorithm (task_2), data-driven from
tests/fixtures/narrative_clusters/prior_run_clusters.yaml.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.cluster import (
    _ClusterIdSequence,
    _match_or_create_cluster_id,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import ClusterRecord

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/prior_run_clusters.yaml")


def _load_fixture() -> dict:
    if not FIXTURE_PATH.exists():
        pytest.skip(f"required fixture missing: {FIXTURE_PATH}")
    return yaml.safe_load(FIXTURE_PATH.read_text())


@pytest.fixture()
def prior_clusters() -> list[ClusterRecord]:
    fixture = _load_fixture()
    return [ClusterRecord(**entry) for entry in fixture["prior_clusters"]]


@pytest.mark.parametrize(
    "case_index",
    range(len(_load_fixture()["match_test_cases"])) if FIXTURE_PATH.exists() else [],
)
def test_match_or_create_cluster_id(prior_clusters: list[ClusterRecord], case_index: int) -> None:
    case = _load_fixture()["match_test_cases"][case_index]
    used_prior_ids: set[str] = set()
    id_sequence = _ClusterIdSequence([c.cluster_id for c in prior_clusters])

    result = _match_or_create_cluster_id(
        case["member_tickers"], case["topic_embedding"], prior_clusters, used_prior_ids, id_sequence
    )

    if case["expected_cluster_id"] is None:
        existing_ids = {c.cluster_id for c in prior_clusters}
        assert result not in existing_ids, f"{case['name']}: expected a newly minted cluster id"
    else:
        assert result == case["expected_cluster_id"], case["name"]
