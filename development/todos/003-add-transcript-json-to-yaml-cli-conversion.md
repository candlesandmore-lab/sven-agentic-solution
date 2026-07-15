# Goal:
Add a CLI-only conversion flow to technical_trader_solution that converts FMP earnings transcript JSON into the YAML document-fixture format used by narrative cluster fixture data, and generate an initial converted YAML file from the existing transcript export.

# Success criteria:
- The technical_trader_solution CLI exposes a conversion command that reads transcript JSON and writes YAML in the same top-level shape used by tests/fixtures/narrative_clusters/documents.yaml.
- The conversion flow is limited to the CLI surface; no SDK, MCP, or dashboard surface is added in this story.
- The generated YAML output for Project_Communication/FMP_Earnings_Transcripts/earnings_transcripts.json is written into Project_Communication/FMP_Earnings_Transcripts/.
- The conversion logic handles the current transcript export format robustly enough for future JSON report conversions through the CLI.
- Tests cover the conversion logic and CLI behavior using repository fixture data or targeted sample inputs.

# Implementation hints:
- Reuse the fixture-document schema from tests/fixtures/narrative_clusters/documents.yaml, especially the documents list entries with ticker, source_type, source_id, published_at, and text.
- Prefer placing the conversion logic inside technical_trader_solution and exposing it through the existing tts CLI rather than as a standalone utility script.
- If a dedicated script is still useful for direct repository maintenance, make it a thin Perl wrapper around the same CLI flow or generated output contract rather than a separate data model.