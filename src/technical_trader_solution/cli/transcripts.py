"""`tts transcripts` command group for local transcript conversion workflows."""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from pathlib import Path

import click

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import SourceType
from technical_trader_solution.core.transcript_conversion import convert_fmp_json_to_yaml
from technical_trader_solution.errors import TechnicalTraderSolutionError, format_error_message

_logger = logging.getLogger("technical_trader_solution")


def _catch_domain_errors(command: Callable) -> Callable:
    """Catch domain exceptions, print the unified message to stderr, exit non-zero."""

    @functools.wraps(command)
    def wrapper(*args, **kwargs):
        try:
            command(*args, **kwargs)
        except TechnicalTraderSolutionError as exc:
            click.echo(format_error_message(exc), err=True)
            raise SystemExit(1) from exc

    return wrapper


@click.group("transcripts")
def transcripts() -> None:
    """Transcript conversion commands."""


@transcripts.command("convert-fmp-json")
@click.argument("input_file_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--output-dir",
    default=None,
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory for the generated YAML file (default: the input file's directory).",
)
@click.option(
    "--source-type",
    default=SourceType.EARNINGS_TRANSCRIPT.value,
    show_default=True,
    type=click.Choice([member.value for member in SourceType], case_sensitive=False),
    help="Source type to write into converted YAML records.",
)
@_catch_domain_errors
def convert_fmp_json(input_file_path: Path, output_dir: Path | None, source_type: str) -> None:
    """Convert one FMP transcript JSON file into canonical fixture-document YAML."""

    resolved_source_type = SourceType(source_type)
    _logger.info(
        "Starting transcript conversion input=%s output_dir=%s source_type=%s",
        input_file_path,
        output_dir,
        resolved_source_type.value,
    )
    output_path, document_count = convert_fmp_json_to_yaml(
        input_file_path,
        output_dir=output_dir,
        source_type=resolved_source_type,
    )
    _logger.info(
        "Completed transcript conversion input=%s output=%s documents=%s",
        input_file_path,
        output_path,
        document_count,
    )
    click.echo(f"Wrote {document_count} document(s) to {output_path}")
