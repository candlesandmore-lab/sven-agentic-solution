"""Root CLI entry point for the Technical Trader Solution (``tts``).

Per-capability command groups are registered here by the task that wires that
capability's invocation surfaces.
"""

from __future__ import annotations

import click

from technical_trader_solution.cli.dashboard import dashboard
from technical_trader_solution.cli.narrative_clusters import narrative
from technical_trader_solution.logging import DEFAULT_LOG_LEVEL, VALID_LOG_LEVELS, configure_logger

__all__ = ["app"]


@click.group()
@click.version_option(package_name="technical-trader-solution")
@click.option(
    "--log-dir",
    default=None,
    help="Directory for the shared log file (default: technical_trader_solution/ in the current directory).",
)
@click.option(
    "--log-level",
    default=DEFAULT_LOG_LEVEL,
    show_default=True,
    type=click.Choice(VALID_LOG_LEVELS, case_sensitive=False),
    help="Logging verbosity.",
)
def app(log_dir: str | None, log_level: str) -> None:
    """Technical Trader Solution command-line interface."""

    configure_logger("technical_trader_solution", log_dir=log_dir, log_level=log_level)


@click.group("mcp")
def mcp_group() -> None:
    """MCP server commands."""


@mcp_group.command("serve")
def mcp_serve() -> None:
    """Serve this workspace's own Technical Trader Solution MCP server."""

    from technical_trader_solution.mcp.server import main as run_mcp_server

    run_mcp_server()


app.add_command(narrative)
app.add_command(mcp_group)
app.add_command(dashboard)
