"""SDK surface for the Narrative Extraction and Clustering Pipeline (story 001, US-015).

Reused as-is by the CLI, MCP, and Discovery Surface -- none of them query
NarrativeClustersStore directly, per the implementation spec's SDK-only data-access
contract.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from technical_trader_solution.coded_agents.narrative_clusters_agent.agent import (
    NarrativeClustersAgent,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.fetch import FetchDocuments
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import ClusterView
from technical_trader_solution.coded_agents.narrative_clusters_agent.storage import (
    DEFAULT_DB_PATH,
    NarrativeClustersStore,
)


def run_nightly_pipeline(
    tickers: list[str],
    *,
    run_date: date | str | None = None,
    db_path: Path | str = DEFAULT_DB_PATH,
    task_id: str | None = None,
    fetch_documents: FetchDocuments | None = None,
) -> dict:
    """Run one nightly narrative-extraction-and-clustering pass for `tickers`.

    Returns the coded agent's response: `status: succeeded` with `output.clusters` (a
    list of trader-facing cluster views), or `status: failed_after_iterations` with
    `questions` to answer and resume with the same `task_id`.
    """

    resolved_run_date = run_date.isoformat() if isinstance(run_date, date) else run_date
    agent = NarrativeClustersAgent(db_path=db_path)
    inputs: dict = {"run_date": resolved_run_date, "tickers": tickers}
    if fetch_documents is not None:
        inputs["fetch_documents"] = fetch_documents
    return agent.run(task_id=task_id or f"nightly-{resolved_run_date or 'today'}", inputs=inputs)


def get_clusters(
    run_date: date | None = None, *, db_path: Path | str = DEFAULT_DB_PATH
) -> list[ClusterView]:
    """Trader-facing clusters for `run_date` (the most recent run when omitted)."""

    store = NarrativeClustersStore(db_path)
    return [ClusterView.from_record(record) for record in store.get_clusters(run_date)]


def get_cluster_trend(cluster_id: str, *, db_path: Path | str = DEFAULT_DB_PATH) -> list[dict]:
    """This cluster's frequency-of-mention/company-breadth trend, oldest run first."""

    store = NarrativeClustersStore(db_path)
    return [snapshot.model_dump(mode="json") for snapshot in store.get_cluster_trend(cluster_id)]
