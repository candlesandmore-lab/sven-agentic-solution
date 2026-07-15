# Development Workspace Docs

This directory is the starting point for agent-dev-agent development work.

## Document locations

- `architecture`: architecture decisions and solution structure.
- `implementation`: implementation specifications and roadmaps.
- `methodology`: development-flow and delivery-methodology notes.
- `schemas`: YAML schemas and templates used by backlog stories and review gates.

## Development locations

- `../development/todos`: raw developer goals and first prompts.
- `../development/backlog/open`: stories ready to be selected.
- `../development/backlog/active`: the story currently being processed.
- `../development/backlog/implemented`: completed story records.

## Methodology document lookup

The methodology corpus is now linked from this index for quick navigation:

- [methodology/glossary.md](methodology/glossary.md) — terminology and corpus definitions.
- [methodology/market-behavior.md](methodology/market-behavior.md) — observable market behaviors.
- [methodology/roles.md](methodology/roles.md) — role definitions used in the corpus.
- [methodology/trading-strategies.md](methodology/trading-strategies.md) — trading responses to observed behaviors.

## Architecture document lookup

- [architecture/01-technical-trader-solution.md](architecture/01-technical-trader-solution.md) — Technical Trader Solution architecture foundations, component topology, and solution-surface classification, established with story 001 (US-015 Narrative-Cluster Discovery Surface).

## Implementation document lookup

- [implementation/01-narrative-cluster-discovery-surface.md](implementation/01-narrative-cluster-discovery-surface.md) — implementation specification for the nightly narrative extraction and clustering pipeline and the Discovery Surface dashboard page (story 001, US-015).
- [implementation/02-logging-and-error-handling.md](implementation/02-logging-and-error-handling.md) — cross-cutting logging and error-handling implementation specification covering the core, CLI, SDK, MCP, and dashboard surfaces (story 002).
- [implementation/03-fmp-transcript-json-to-yaml-cli-conversion.md](implementation/03-fmp-transcript-json-to-yaml-cli-conversion.md) — implementation specification for the CLI-only FMP transcript JSON to canonical fixture-document YAML conversion flow (story 003).

