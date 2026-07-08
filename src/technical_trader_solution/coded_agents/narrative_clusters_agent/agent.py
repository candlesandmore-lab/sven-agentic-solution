"""Narrative Extraction and Clustering Pipeline coded agent.

Implements docs/implementation/01-narrative-cluster-discovery-surface.md's Coded-Agent
Flow on the workspace's uniform ClaudeCode SDK base
(technical_trader_solution.coded_agents.base): the fetch/extract/cluster/label/trend/
persist sequence is one `run_generate` iteration, and `evaluate` checks the flow's
documented success criteria. Refine re-runs the whole pipeline (idempotent: fetch uses
each ticker's stored watermark, and storage writes are INSERT OR REPLACE), capped at five
iterations by the base class.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime
from pathlib import Path
from typing import Any

import anthropic

from technical_trader_solution.coded_agents.base import (
    ClaudeCodeSDKAgentBase,
    CodedAgentState,
    EvaluationResult,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.cluster import (
    build_clusters,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.extract import (
    extract_narrative_findings,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.fetch import (
    FMPClient,
    FetchDocuments,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.label import (
    generate_topic_label,
    validate_label,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import RawDocument
from technical_trader_solution.coded_agents.narrative_clusters_agent.storage import (
    DEFAULT_DB_PATH,
    NarrativeClustersStore,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.trend import (
    build_trend_snapshots,
)

MAX_EXCERPTS_PER_CLUSTER = 3
EXCERPT_CHARS = 200


class NarrativeClustersAgent(ClaudeCodeSDKAgentBase):
    """Coded agent for story 001's nightly narrative extraction and clustering run."""

    agent_slug = "narrative-clusters-agent"

    def __init__(
        self,
        *,
        db_path: Path | str = DEFAULT_DB_PATH,
        anthropic_client: anthropic.Anthropic | None = None,
        **base_kwargs: Any,
    ) -> None:
        super().__init__(**base_kwargs)
        self.store = NarrativeClustersStore(db_path)
        self.anthropic_client = anthropic_client

    def run_generate(self, state: CodedAgentState) -> dict[str, Any]:
        inputs = state.inputs
        run_date: date = _parse_run_date(inputs.get("run_date"))
        tickers: list[str] = inputs["tickers"]
        fetch_documents: FetchDocuments = inputs.get("fetch_documents") or FMPClient().fetch_documents

        all_documents: list[RawDocument] = []
        for ticker in tickers:
            since = self.store.latest_watermark(ticker)
            all_documents.extend(fetch_documents(ticker, since))

        findings = extract_narrative_findings(all_documents)
        self.store.save_findings(findings, run_date)

        prior_clusters = self.store.get_prior_run_clusters(before=run_date)
        clusters = build_clusters(
            findings,
            run_date,
            prior_clusters,
            all_known_cluster_ids=self.store.all_cluster_ids(),
        )

        excerpts_by_ticker: dict[str, list[str]] = {}
        for document in all_documents:
            excerpts_by_ticker.setdefault(document.ticker, []).append(document.text[:EXCERPT_CHARS])

        labeled_clusters = []
        for cluster in clusters:
            top_keyphrases = [w.strip() for w in cluster.topic_label.split(",")]
            excerpts: list[str] = []
            for ticker in cluster.member_tickers:
                excerpts.extend(excerpts_by_ticker.get(ticker, []))
                if len(excerpts) >= MAX_EXCERPTS_PER_CLUSTER:
                    break
            label = generate_topic_label(
                top_keyphrases, excerpts[:MAX_EXCERPTS_PER_CLUSTER], client=self.anthropic_client
            )
            labeled_clusters.append(cluster.model_copy(update={"topic_label": label}))

        self.store.save_clusters(labeled_clusters)
        trend_snapshots = build_trend_snapshots(labeled_clusters)
        self.store.save_trend_snapshots(trend_snapshots)

        return {
            "run_date": run_date.isoformat(),
            "documents_fetched": len(all_documents),
            "findings_count": len(findings),
            "clusters": [cluster.model_dump(mode="json") for cluster in labeled_clusters],
        }

    def evaluate(self, state: CodedAgentState, output: dict[str, Any]) -> EvaluationResult:
        if output.get("documents_fetched", 0) > 0 and output.get("findings_count", 0) == 0:
            return EvaluationResult(
                passed=False,
                feedback="Documents were fetched but no narrative findings were extracted.",
            )

        for cluster in output.get("clusters", []):
            if not cluster.get("member_tickers"):
                return EvaluationResult(
                    passed=False, feedback=f"Cluster {cluster.get('cluster_id')} has no members."
                )
            if not validate_label(cluster.get("topic_label", "")):
                return EvaluationResult(
                    passed=False,
                    feedback=f"Cluster {cluster.get('cluster_id')} has an invalid topic label.",
                )

        return EvaluationResult(passed=True, feedback="Run produced valid clusters, labels, and trend snapshots.")


def _parse_run_date(value: str | date | None) -> date:
    if value is None:
        return datetime.now().date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)
