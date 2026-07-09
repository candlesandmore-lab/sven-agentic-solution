"""MCP tools for the Narrative Extraction and Clustering Pipeline (story 001, US-015).

Registered on the shared `mcp` server instance from `technical_trader_solution.mcp.server`.
Reuses the same technical_trader_solution.sdk.narrative_clusters functions as the CLI and
SDK surfaces. Registered in this workspace's own local MCP server/config, not packaged as
a distributable instructed-agent asset (see docs/implementation/
01-narrative-cluster-discovery-surface.md, Interface Contracts).
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from technical_trader_solution.mcp.server import mcp
from technical_trader_solution.sdk.narrative_clusters import (
    get_cluster_trend,
    get_clusters,
    run_nightly_pipeline,
)


class RunNightlyPipelineRequest(BaseModel):
    tickers: list[str]
    run_date: str | None = None


class GetClustersRequest(BaseModel):
    run_date: str | None = None


class GetClusterTrendRequest(BaseModel):
    cluster_id: str


@mcp.tool()
def narrative_run_nightly_pipeline(request: RunNightlyPipelineRequest) -> dict:
    """Run one nightly narrative-extraction-and-clustering pass for the given tickers."""

    return run_nightly_pipeline(request.tickers, run_date=request.run_date)


@mcp.tool()
def narrative_get_clusters(request: GetClustersRequest) -> list[dict]:
    """Trader-facing clusters for a run date (the most recent run when omitted)."""

    run_date = date.fromisoformat(request.run_date) if request.run_date else None
    return [cluster.model_dump(mode="json") for cluster in get_clusters(run_date)]


@mcp.tool()
def narrative_get_cluster_trend(request: GetClusterTrendRequest) -> list[dict]:
    """A cluster's frequency-of-mention/company-breadth trend, oldest run first."""

    return get_cluster_trend(request.cluster_id)
