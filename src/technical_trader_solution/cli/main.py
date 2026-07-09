"""Root CLI entry point for the Technical Trader Solution (``tts``).

Per-capability command groups are registered here by the task that wires that
capability's invocation surfaces.
"""

from __future__ import annotations

import click

from technical_trader_solution.cli.dashboard import dashboard
from technical_trader_solution.cli.narrative_clusters import narrative

__all__ = ["app"]


@click.group()
@click.version_option(package_name="technical-trader-solution")
def app() -> None:
    """Technical Trader Solution command-line interface."""


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
