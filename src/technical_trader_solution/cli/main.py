"""Root CLI entry point for the Technical Trader Solution (``tts``).

Per-capability command groups (for example ``tts narrative`` and ``tts dashboard``) are
registered here by the task that wires that capability's invocation surfaces. This module
is a scaffold placeholder: it defines the root group and version output only.
"""

from __future__ import annotations

import click

__all__ = ["app"]


@click.group()
@click.version_option(package_name="technical-trader-solution")
def app() -> None:
    """Technical Trader Solution command-line interface."""
