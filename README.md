# Technical Trader Solution

An agentic solution supporting a human trader's trading strategies, built with
`agent-dev-agent` from the todos in `development/todos` and the methodology corpus in
`docs/methodology`. See `docs/README.md` for the full documentation index.

## Quick start

```sh
uv venv
uv sync
uv run pytest
```

## CLI

The `tts` command is the Technical Trader Solution's own command-line interface (distinct
from `agent-building-agent`'s CLI, which manages the development flow itself):

```sh
uv run tts --help
```

## Structure

- `src/technical_trader_solution/core` — shared core logic, reused by `sdk`, `cli`, and `mcp`.
- `src/technical_trader_solution/sdk` — Python SDK surface.
- `src/technical_trader_solution/cli` — the `tts` command-line interface.
- `src/technical_trader_solution/mcp` — the Technical Trader Solution's own MCP server.
- `tests/{unit,sdk,cli,mcp,prompts,fixtures}` — tests and data-driven fixtures, one
  fixtures subdirectory per capability (for example `tests/fixtures/narrative_clusters`).
- `demos` — runnable demonstrations for each capability.
