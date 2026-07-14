"""Prompt-validation test for the label node (task_5).

Per docs/implementation/01-narrative-cluster-discovery-surface.md's Interface Contracts:
the label node's output is a single short string (not a JSON payload, unlike the four
framework coded agents), so its validation and refinement contract is exercised here
rather than assumed to match those agents' structured-JSON tests.

Three layers, per the QA prompt-validation requirement:
1. `validate_label` (the evaluate-node check) against malformed/valid single-string
   candidates -- deterministic, no API key required.
2. `NarrativeClustersAgent.evaluate()` triggers refinement (passed=False) for an
   otherwise-valid run whose only defect is an invalid cluster label, and passes a
   run whose label is valid -- deterministic, no API key required.
3. `generate_topic_label` against the real Anthropic API, confirming the live single-
   string output contract (no JSON wrapper, no multi-line output, within the length
   bound). Marked `live_endpoint`; skips when ANTHROPIC_API_KEY is not configured.
   Developer approval of this live evidence is required before this checkpoint is
   considered accepted, per the QA approval-boundaries sub-skill.
"""

from __future__ import annotations

import os

import pytest

from technical_trader_solution.coded_agents.narrative_clusters_agent.agent import (
    NarrativeClustersAgent,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.label import (
    MAX_LABEL_CHARS,
    generate_topic_label,
    validate_label,
)


@pytest.mark.parametrize(
    "label,expected_valid",
    [
        ("AI datacenter power surge", True),
        ("Quantum computing progress and milestones", True),
        ("", False),
        ("x" * (MAX_LABEL_CHARS + 1), False),
        ("x" * MAX_LABEL_CHARS, True),
    ],
)
def test_validate_label(label: str, expected_valid: bool) -> None:
    assert validate_label(label) is expected_valid


def test_agent_evaluate_rejects_invalid_label(tmp_path) -> None:
    agent = NarrativeClustersAgent(
        db_path=tmp_path / "narrative_clusters.sqlite",
        state_db_path=tmp_path / "narrative-clusters-agent-state.sqlite",
        log_dir=tmp_path,
    )
    output = {
        "documents_fetched": 2,
        "findings_count": 2,
        "clusters": [
            {
                "cluster_id": "cluster-0001",
                "member_tickers": ["NVDA", "VST"],
                "topic_label": "",
                "frequency_of_mention": 2,
                "company_breadth": 2,
            }
        ],
    }
    result = agent.evaluate(state=None, output=output)
    assert result.passed is False
    assert "invalid topic label" in result.feedback.lower()


def test_agent_evaluate_accepts_valid_label(tmp_path) -> None:
    agent = NarrativeClustersAgent(
        db_path=tmp_path / "narrative_clusters.sqlite",
        state_db_path=tmp_path / "narrative-clusters-agent-state.sqlite",
        log_dir=tmp_path,
    )
    output = {
        "documents_fetched": 2,
        "findings_count": 2,
        "clusters": [
            {
                "cluster_id": "cluster-0001",
                "member_tickers": ["NVDA", "VST"],
                "topic_label": "AI datacenter power surge",
                "frequency_of_mention": 2,
                "company_breadth": 2,
            }
        ],
    }
    result = agent.evaluate(state=None, output=output)
    assert result.passed is True


@pytest.mark.live_endpoint
def test_generate_topic_label_live_single_string_contract() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        pytest.skip("ANTHROPIC_API_KEY not configured")

    label = generate_topic_label(
        top_keyphrases=["datacenter", "power demand", "ai datacenter"],
        excerpts=[
            "Datacenter demand for our GPU accelerators remains extremely strong as "
            "hyperscale customers build out massive AI datacenter capacity.",
            "We are seeing unprecedented power demand from AI datacenter operators "
            "seeking to secure long-term power purchase agreements.",
        ],
    )

    assert validate_label(label)
    assert "\n" not in label, "label node's contract is a single line, not multi-line"
    assert not label.strip().startswith("{"), "label node's contract is a string, not JSON"
    assert len(label) <= MAX_LABEL_CHARS
