# FMP Transcript JSON to YAML CLI Conversion Implementation Specification

## Purpose

Define the implementation contract for story 003
(`development/todos/003-add-transcript-json-to-yaml-cli-conversion.md`): a CLI-only
conversion flow that turns FMP earnings transcript JSON exports into the canonical
fixture-document YAML format used by
`tests/fixtures/narrative_clusters/documents.yaml`.

## Architecture impact

- No architecture-document update is required for this story.
- Rationale: the existing architecture already permits reusable Python core logic and CLI
  entry points inside the Technical Trader Solution. This story adds a local utility
  command only; it does not alter the solution's delivery interface, component topology,
  or solution-surface classification.

## Scope

### In scope

- A new CLI group and command: `tts transcripts convert-fmp-json <input-file-path>
  [--output-dir <dir>] [--source-type <value>]`.
- A reusable internal conversion module under `src/technical_trader_solution/`.
- Strict validation of the input JSON structure and the emitted YAML structure.
- Timestamped YAML output written beside the source file by default, or into an explicit
  output directory.
- Detailed CLI validation failures and shared logging/error-handling integration.
- Repository tests for success cases, malformed input failures, and CLI wiring.
- One generated YAML artifact for
  `Project_Communication/FMP_Earnings_Transcripts/earnings_transcripts.json`.

### Out of scope

- SDK, MCP, dashboard, or Perl-wrapper surfaces.
- Batch conversion of multiple input files, directories, or glob patterns.
- Downstream narrative extraction, keyphrase/entity generation, clustering, or cluster
  trend computation.
- Any output shape other than the canonical fixture-document format.

## Invocation surface contract

- Included surface:
  - CLI.
- Explicitly omitted surfaces:
  - SDK: omitted; this story is a one-shot local conversion utility, not a trader-facing
    library API.
  - MCP: omitted; the workflow is file conversion, not an interactive tool-call surface.
  - Dashboard: omitted; there is no dashboard use case for this story.
  - Perl wrapper: omitted; user approved CLI-only implementation.

## CLI contract

- Command: `tts transcripts convert-fmp-json`.
- Required positional argument:
  - `<input-file-path>`: path to a single FMP transcript JSON file.
- Optional arguments:
  - `--output-dir <dir>`: directory for the emitted YAML file. Defaults to the input
    file's directory.
  - `--source-type <value>`: defaults to `earnings_transcript`; accepted values follow
    the existing `SourceType` enum (`earnings_transcript`, `sec_filing`, `news`).
  - `--log-dir <dir>` and `--log-level [info|debug|warning|error]`: inherited from the
    root `tts` CLI contract.
- Single-file only: the command accepts exactly one JSON input file per invocation.

## Input JSON contract

- The input file must parse as a JSON object.
- The top-level object must map ticker symbols to arrays of transcript records.
- Each transcript record must include:
  - `symbol`: string.
  - `quarter`: integer.
  - `year`: integer.
  - `date`: string formatted as `YYYY-MM-DD HH:MM:SS`.
  - `content`: non-empty string.
- Validation rules:
  - The top-level key and each record's `symbol` must match exactly.
  - `quarter` must be an integer in `1..4`.
  - `year` must be a four-digit integer.
  - `date` must parse with `datetime.strptime(value, "%Y-%m-%d %H:%M:%S")`.
  - `content` must remain non-empty after trimming surrounding whitespace.
- Failure mode:
  - Fail fast on the first malformed or incomplete record.
  - Raise a domain exception carrying a detailed validation message that identifies the
    ticker, record index, and failing field.

## Output YAML contract

- The output must match the canonical fixture-document format at
  `tests/fixtures/narrative_clusters/documents.yaml`.
- Structure:

```yaml
documents:
  - ticker: EXAMPLE
    source_type: earnings_transcript
    source_id: EXAMPLE-transcript-2026-q2
    published_at: "2026-03-18T16:30:00"
    text: >
      Transcript text
```

- Required fields per document entry:
  - `ticker`: string, copied from `symbol`.
  - `source_type`: enum, taken from `--source-type` with default `earnings_transcript`.
  - `source_id`: string derived as `{symbol}-transcript-{year}-q{quarter}`.
  - `published_at`: naive ISO datetime string `YYYY-MM-DDTHH:MM:SS`, converted from the
    input `date` value.
  - `text`: string copied from `content`.
- Ordering:
  - Preserve the source file's ticker iteration order and per-ticker record order.

## Output file contract

- Filename pattern: `{input_stem}_{timestamp}.yaml`.
- Timestamp format: `YYYY-MM-DDTHH-MM-SS`.
- Default output directory: the input file's parent directory.
- Collision policy:
  - Second-level precision is the baseline. If a same-name file already exists, append a
    numeric suffix before the `.yaml` extension.

## Logging and error handling

- Reuse the story-002 logging contract already implemented in
  `technical_trader_solution.logging` and `technical_trader_solution.errors`.
- The new command must:
  - Log invocation start at `INFO`.
  - Log successful completion with input path, output path, and converted record count at
    `INFO`.
  - Raise domain exceptions from the conversion core for invalid input, invalid output, or
    filesystem write failures.
  - Catch domain exceptions at the CLI boundary and print the unified error message to
    stderr with non-zero exit.

## Suggested module layout

- `src/technical_trader_solution/core/transcript_conversion.py`
  - input/output data models.
  - parsing and validation helpers.
  - JSON-to-document conversion function.
  - YAML serialization and output-path generation.
- `src/technical_trader_solution/cli/transcripts.py`
  - `tts transcripts` command group.
  - `convert-fmp-json` command.

## Validation expectations

- Unit tests:
  - valid single-file conversion produces the expected document entries.
  - malformed top-level structure fails.
  - mismatched ticker/symbol fails.
  - empty content fails.
  - invalid quarter/date fails.
  - source_id and published_at mapping are deterministic.
- CLI tests:
  - success path writes a timestamped YAML file.
  - failure path exits non-zero with a unified error message.
  - `--source-type` override is honored.
- Generated artifact check:
  - run the CLI against
    `Project_Communication/FMP_Earnings_Transcripts/earnings_transcripts.json` and verify
    a YAML file appears in the same directory.
