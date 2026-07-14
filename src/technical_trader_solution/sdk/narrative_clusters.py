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
from technical_trader_solution.errors import InvalidClusterError
from technical_trader_solution.logging import DEFAULT_LOG_LEVEL, configure_logger


def configure_logging(
    *, log_dir: str | Path | None = None, log_level: str = DEFAULT_LOG_LEVEL
):
    """Configure the shared logger for an embedding process that does not go through the
    CLI. Call once at process startup, before any other SDK function, per the Logging
    Contract's SDK section -- SDK functions do not call `configure_logger` themselves."""

    return configure_logger("technical_trader_solution", log_dir=log_dir, log_level=log_level)


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
    """This cluster's frequency-of-mention/company-breadth trend, oldest run first.

    Raises `InvalidClusterError` when `cluster_id` has never existed; returns an empty
    list when the cluster exists but has no trend snapshots yet.
    """

    store = NarrativeClustersStore(db_path)
    if cluster_id not in store.all_cluster_ids():
        raise InvalidClusterError(f"cluster_id {cluster_id!r} does not exist.")
    return [snapshot.model_dump(mode="json") for snapshot in store.get_cluster_trend(cluster_id)]
