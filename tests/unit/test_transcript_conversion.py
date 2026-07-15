from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import SourceType
from technical_trader_solution.core.transcript_conversion import (
    build_output_path,
    convert_fmp_json_to_yaml,
    load_fmp_transcripts,
)
from technical_trader_solution.errors import ConversionError


def _write_input_file(tmp_path: Path, payload: dict) -> Path:
    input_path = tmp_path / "earnings_transcripts.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    return input_path


def test_load_fmp_transcripts_maps_records_to_raw_documents(tmp_path: Path) -> None:
    input_path = _write_input_file(
        tmp_path,
        {
            "MU": [
                {
                    "symbol": "MU",
                    "quarter": 2,
                    "year": 2026,
                    "date": "2026-03-18 16:30:00",
                    "content": "Transcript body",
                }
            ]
        },
    )

    documents = load_fmp_transcripts(input_path, SourceType.EARNINGS_TRANSCRIPT)

    assert len(documents) == 1
    assert documents[0].ticker == "MU"
    assert documents[0].source_id == "MU-transcript-2026-q2"
    assert documents[0].published_at == datetime(2026, 3, 18, 16, 30, 0)
    assert documents[0].source_type is SourceType.EARNINGS_TRANSCRIPT


def test_load_fmp_transcripts_rejects_mismatched_symbol(tmp_path: Path) -> None:
    input_path = _write_input_file(
        tmp_path,
        {
            "MU": [
                {
                    "symbol": "AMD",
                    "quarter": 2,
                    "year": 2026,
                    "date": "2026-03-18 16:30:00",
                    "content": "Transcript body",
                }
            ]
        },
    )

    with pytest.raises(ConversionError, match="mismatched symbol"):
        load_fmp_transcripts(input_path, SourceType.EARNINGS_TRANSCRIPT)


def test_convert_fmp_json_to_yaml_writes_canonical_documents_payload(tmp_path: Path) -> None:
    input_path = _write_input_file(
        tmp_path,
        {
            "MU": [
                {
                    "symbol": "MU",
                    "quarter": 2,
                    "year": 2026,
                    "date": "2026-03-18 16:30:00",
                    "content": "Transcript body",
                }
            ]
        },
    )

    output_path, document_count = convert_fmp_json_to_yaml(
        input_path,
        output_dir=tmp_path,
        source_type=SourceType.NEWS,
        now=datetime(2026, 7, 15, 14, 30, 0),
    )

    assert document_count == 1
    assert output_path.name == "earnings_transcripts_2026-07-15T14-30-00.yaml"

    payload = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    assert list(payload) == ["documents"]
    assert payload["documents"] == [
        {
            "ticker": "MU",
            "source_type": "news",
            "source_id": "MU-transcript-2026-q2",
            "published_at": "2026-03-18T16:30:00",
            "text": "Transcript body",
        }
    ]


def test_build_output_path_adds_suffix_when_timestamped_name_exists(tmp_path: Path) -> None:
    input_path = tmp_path / "earnings_transcripts.json"
    input_path.write_text("{}", encoding="utf-8")
    existing = tmp_path / "earnings_transcripts_2026-07-15T14-30-00.yaml"
    existing.write_text("documents: []\n", encoding="utf-8")

    output_path = build_output_path(input_path, now=datetime(2026, 7, 15, 14, 30, 0))

    assert output_path.name == "earnings_transcripts_2026-07-15T14-30-00_1.yaml"
