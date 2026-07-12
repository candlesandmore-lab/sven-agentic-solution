"""`tts dashboard` command group (story 001, US-015).

Launches the Streamlit-based Discovery Surface page via a subprocess `streamlit run`
call, forwarding dashboard-specific options to the page script after `--` (Streamlit's
own convention for script arguments), per docs/implementation/
01-narrative-cluster-discovery-surface.md's Discovery Surface section.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click

from technical_trader_solution.coded_agents.narrative_clusters_agent.storage import (
    DEFAULT_DB_PATH,
)
from technical_trader_solution.logging import DEFAULT_LOG_FILE, DEFAULT_LOG_LEVEL

DISCOVERY_SURFACE_PAGE = Path(__file__).parent.parent / "dashboard" / "discovery_surface.py"


@click.group("dashboard")
def dashboard() -> None:
    """Local web dashboard commands."""


@dashboard.command("serve")
@click.option("--port", default=8501, show_default=True, help="Port to serve the dashboard on.")
@click.option(
    "--db-path",
    default=str(DEFAULT_DB_PATH),
    show_default=True,
    help="Path to the narrative_clusters SQLite store.",
)
@click.option("--log-file", default=DEFAULT_LOG_FILE, show_default=True, help="Dashboard log file path.")
@click.option("--log-level", default=DEFAULT_LOG_LEVEL, show_default=True, help="Dashboard log level.")
def serve(port: int, db_path: str, log_file: str, log_level: str) -> None:
    """Serve the Discovery Surface page of the Technical Trader Solution dashboard."""

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(DISCOVERY_SURFACE_PAGE),
        "--server.port",
        str(port),
        "--",
        "--db-path",
        db_path,
        "--log-file",
        log_file,
        "--log-level",
        log_level,
    ]
    raise SystemExit(subprocess.call(command))
