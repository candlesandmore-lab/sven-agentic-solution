from __future__ import annotations

import json
from pathlib import Path

import yaml
from click.testing import CliRunner

from technical_trader_solution.cli.main import app


def _write_input_file(tmp_path: Path, payload: dict) -> Path:
    input_path = tmp_path / "earnings_transcripts.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    return input_path


def test_cli_convert_fmp_json_writes_yaml_file(tmp_path: Path) -> None:
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
    output_dir = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--log-dir",
            str(tmp_path / "logs"),
            "transcripts",
            "convert-fmp-json",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--source-type",
            "news",
        ],
    )

    assert result.exit_code == 0, result.output
    written_files = list(output_dir.glob("*.yaml"))
    assert len(written_files) == 1
    payload = yaml.safe_load(written_files[0].read_text(encoding="utf-8"))
    assert payload["documents"][0]["source_type"] == "news"
    assert "Wrote 1 document(s) to" in result.output


def test_cli_convert_fmp_json_exits_nonzero_with_unified_error(tmp_path: Path) -> None:
    input_path = _write_input_file(
        tmp_path,
        {
            "MU": [
                {
                    "symbol": "MU",
                    "quarter": 5,
                    "year": 2026,
                    "date": "2026-03-18 16:30:00",
                    "content": "Transcript body",
                }
            ]
        },
    )

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--log-dir",
            str(tmp_path / "logs"),
            "transcripts",
            "convert-fmp-json",
            str(input_path),
        ],
    )

    assert result.exit_code == 1
    assert "Conversion:" in result.output
    assert "quarter must be one of 1, 2, 3, or 4" in result.output
    assert "Traceback" not in result.output