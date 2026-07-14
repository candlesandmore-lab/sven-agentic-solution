"""`tts dashboard` command group (story 001, US-015).

Launches the Streamlit-based Discovery Surface page via a subprocess `streamlit run`
call, forwarding dashboard-specific options to the page script after `--` (Streamlit's
own convention for script arguments), per docs/implementation/
01-narrative-cluster-discovery-surface.md's Discovery Surface section.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import click

from technical_trader_solution.coded_agents.narrative_clusters_agent.storage import (
    DEFAULT_DB_PATH,
)
from technical_trader_solution.logging import (
    DEFAULT_LOG_LEVEL,
    RUN_TIMESTAMP_ENV_VAR,
    VALID_LOG_LEVELS,
    resolve_run_timestamp,
)

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
@click.option("--log-dir", default=None, help="Directory for the shared log file (default: technical_trader_solution/ in the current directory).")
@click.option(
    "--log-level",
    default=DEFAULT_LOG_LEVEL,
    show_default=True,
    type=click.Choice(VALID_LOG_LEVELS, case_sensitive=False),
    help="Logging verbosity.",
)
def serve(port: int, db_path: str, log_dir: str | None, log_level: str) -> None:
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
        "--log-level",
        log_level,
    ]
    if log_dir is not None:
        command.extend(["--log-dir", log_dir])

    # Resolve TTS_RUN_TIMESTAMP in this process and pass it through the subprocess
    # environment, so the streamlit subprocess's own configure_logger call reuses it
    # instead of minting a new one, per the run-scoping guardrail for nested processes.
    env = dict(os.environ)
    env[RUN_TIMESTAMP_ENV_VAR] = resolve_run_timestamp()
    raise SystemExit(subprocess.call(command, env=env))
