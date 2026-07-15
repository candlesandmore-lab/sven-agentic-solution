"""Conversion helpers for FMP transcript JSON to canonical fixture-document YAML."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError, field_validator

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import RawDocument, SourceType
from technical_trader_solution.errors import ConversionError

INPUT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
OUTPUT_TIMESTAMP_FORMAT = "%Y-%m-%dT%H-%M-%S"


class FmpTranscriptRecord(BaseModel):
    """One transcript record from the FMP export."""

    symbol: str
    quarter: int
    year: int
    date: str
    content: str

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("symbol must be non-empty")
        return value

    @field_validator("quarter")
    @classmethod
    def validate_quarter(cls, value: int) -> int:
        if value not in {1, 2, 3, 4}:
            raise ValueError("quarter must be one of 1, 2, 3, or 4")
        return value

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value < 1000 or value > 9999:
            raise ValueError("year must be a four-digit integer")
        return value

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        try:
            datetime.strptime(value, INPUT_DATE_FORMAT)
        except ValueError as exc:
            raise ValueError(f"date must match {INPUT_DATE_FORMAT}") from exc
        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("content must be non-empty")
        return value

    def published_at(self) -> datetime:
        return datetime.strptime(self.date, INPUT_DATE_FORMAT)

    def source_id(self) -> str:
        return f"{self.symbol}-transcript-{self.year}-q{self.quarter}"


class FixtureDocumentFile(BaseModel):
    """Top-level YAML document contract for the fixture-document format."""

    documents: list[RawDocument]


def _read_json_file(input_path: Path) -> Any:
    try:
        return json.loads(input_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConversionError(f"Unable to read input file {input_path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ConversionError(f"Input file {input_path} is not valid JSON: {exc}") from exc


def load_fmp_transcripts(input_path: Path, source_type: SourceType) -> list[RawDocument]:
    """Load one FMP transcript JSON export into validated RawDocument records."""

    raw = _read_json_file(input_path)
    if not isinstance(raw, dict):
        raise ConversionError("Input JSON must be a top-level object mapping tickers to transcript lists")

    documents: list[RawDocument] = []
    for ticker, records in raw.items():
        if not isinstance(ticker, str) or not ticker.strip():
            raise ConversionError("Each top-level JSON key must be a non-empty ticker string")
        if not isinstance(records, list):
            raise ConversionError(f"Ticker {ticker} must map to a list of transcript records")

        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise ConversionError(f"Ticker {ticker} record {index} must be a JSON object")
            try:
                parsed = FmpTranscriptRecord.model_validate(record)
            except ValidationError as exc:
                raise ConversionError(f"Ticker {ticker} record {index} failed validation: {exc}") from exc

            if parsed.symbol != ticker:
                raise ConversionError(
                    f"Ticker {ticker} record {index} has mismatched symbol {parsed.symbol!r}"
                )

            documents.append(
                RawDocument(
                    ticker=parsed.symbol,
                    source_type=source_type,
                    source_id=parsed.source_id(),
                    published_at=parsed.published_at(),
                    text=parsed.content,
                )
            )

    if not documents:
        raise ConversionError("Input JSON contained no transcript records")
    return documents


def build_output_path(input_path: Path, output_dir: Path | None = None, now: datetime | None = None) -> Path:
    """Build a timestamped, collision-safe YAML output path."""

    timestamp = (now or datetime.now()).strftime(OUTPUT_TIMESTAMP_FORMAT)
    destination_dir = output_dir or input_path.parent
    candidate = destination_dir / f"{input_path.stem}_{timestamp}.yaml"
    suffix = 1
    while candidate.exists():
        candidate = destination_dir / f"{input_path.stem}_{timestamp}_{suffix}.yaml"
        suffix += 1
    return candidate


def write_fixture_documents_yaml(documents: list[RawDocument], output_path: Path) -> None:
    """Validate and write the canonical fixture-document YAML file."""

    try:
        payload = FixtureDocumentFile(documents=documents)
    except ValidationError as exc:
        raise ConversionError(f"Output payload failed validation: {exc}") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(
            yaml.safe_dump(payload.model_dump(mode="json"), sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
    except OSError as exc:
        raise ConversionError(f"Unable to write output file {output_path}: {exc}") from exc


def convert_fmp_json_to_yaml(
    input_path: Path,
    *,
    output_dir: Path | None = None,
    source_type: SourceType = SourceType.EARNINGS_TRANSCRIPT,
    now: datetime | None = None,
) -> tuple[Path, int]:
    """Convert one FMP transcript export file into canonical fixture-document YAML."""

    documents = load_fmp_transcripts(input_path, source_type)
    output_path = build_output_path(input_path, output_dir=output_dir, now=now)
    write_fixture_documents_yaml(documents, output_path)
    return output_path, len(documents)
