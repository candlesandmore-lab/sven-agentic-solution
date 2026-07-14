"""`tts narrative` command group (story 001, US-015).

Reuses the same technical_trader_solution.sdk.narrative_clusters functions as the SDK
and MCP surfaces.
"""

from __future__ import annotations

import functools
import json
from collections.abc import Callable

import click

from technical_trader_solution.errors import TechnicalTraderSolutionError, format_error_message
from technical_trader_solution.sdk.narrative_clusters import (
    get_cluster_trend,
    get_clusters,
    run_nightly_pipeline,
)


def _catch_domain_errors(command: Callable) -> Callable:
    """Catch `TechnicalTraderSolutionError`, print the unified message to stderr, exit 1."""

    @functools.wraps(command)
    def wrapper(*args, **kwargs):
        try:
            command(*args, **kwargs)
        except TechnicalTraderSolutionError as exc:
            click.echo(format_error_message(exc), err=True)
            raise SystemExit(1) from exc

    return wrapper


@click.group("narrative")
def narrative() -> None:
    """Narrative-cluster discovery commands."""


@narrative.command("run-nightly")
@click.option("--ticker", "tickers", multiple=True, required=True, help="Repeatable: ticker to include in this run.")
@click.option("--run-date", default=None, help="Run date (YYYY-MM-DD); defaults to today.")
@_catch_domain_errors
def run_nightly(tickers: tuple[str, ...], run_date: str | None) -> None:
    """Run one nightly narrative-extraction-and-clustering pass."""

    result = run_nightly_pipeline(list(tickers), run_date=run_date)
    if result["status"] != "succeeded":
        click.echo(f"Run did not succeed after {len(result['attempts'])} attempts:", err=True)
        for question in result["questions"]:
            click.echo(f"  - {question}", err=True)
        raise SystemExit(1)

    clusters = result["output"]["clusters"]
    click.echo(f"Run date {result['output']['run_date']}: {len(clusters)} cluster(s) found.")
    for cluster in clusters:
        click.echo(
            f"  {cluster['cluster_id']}: {cluster['topic_label']} "
            f"({', '.join(cluster['member_tickers'])}) "
            f"mentions={cluster['frequency_of_mention']} breadth={cluster['company_breadth']}"
        )


@narrative.command("show-clusters")
@click.option("--run-date", default=None, help="Run date (YYYY-MM-DD); defaults to the most recent run.")
@_catch_domain_errors
def show_clusters(run_date: str | None) -> None:
    """Show clusters for a run date."""

    from datetime import date as date_cls

    clusters = get_clusters(date_cls.fromisoformat(run_date) if run_date else None)
    if not clusters:
        click.echo("No clusters found.")
        return
    for cluster in clusters:
        click.echo(json.dumps(cluster.model_dump(mode="json")))


@narrative.command("show-trend")
@click.argument("cluster_id")
@_catch_domain_errors
def show_trend(cluster_id: str) -> None:
    """Show a cluster's frequency-of-mention/company-breadth trend over time."""

    trend = get_cluster_trend(cluster_id)
    if not trend:
        click.echo(f"No trend data for {cluster_id}.")
        return
    for snapshot in trend:
        click.echo(json.dumps(snapshot))
