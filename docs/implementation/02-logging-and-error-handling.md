# Logging and Error Handling Implementation Specification

## Purpose

Define the implementation contract for story 002 (development/todos/002-enhance-error-and-logging.md):
cross-cutting error handling and structured logging for every existing Technical Trader Solution
surface (core, coded agents, CLI, SDK, MCP, and the Streamlit dashboard), per
`docs/architecture/01-technical-trader-solution.md`'s Logging and Error Handling section (v0.4).

## Scope

### In scope

- Extending `technical_trader_solution.logging` with datetime-stamped log filenames, a
  configurable log directory, and a configurable log level.
- A domain-exception hierarchy raised by the core layer and handled per surface.
- `--log-dir` and `--log-level` options on every CLI command group, the SDK's configuration
  entry points, the MCP server's startup, and the dashboard launch command.
- A masked-fields utility applied wherever log records or error messages could otherwise include
  a sensitive value.
- A unified CLI/MCP error-message format.
- Instrumenting the existing `narrative_clusters` capability's core, CLI, SDK, MCP, and dashboard
  code with the above, without changing its computed outputs.

### Out of scope

- Any change to the narrative extraction, clustering, labeling, or trend-computation algorithms
  themselves (story 001's logic stays as-is, per this story's guidelines).
- Log retention, rotation, or cleanup tooling (architecture v0.4 explicitly rules this out).
- New capabilities or dashboard pages beyond instrumenting what already exists.

## Logging Contract

- Module: extend `technical_trader_solution/logging.py` (`configure_logger`), not a new module,
  since it already exists and is imported from `narrative_clusters_agent/agent.py` and the CLI
  entry points; a new module would fragment the single logging entry point the architecture
  requires.
- Run-timestamp coordination: `configure_logger` resolves one timestamp per run via an
  inherited-environment-variable-first check on `TTS_RUN_TIMESTAMP` -- if that variable is
  already set (by an earlier `configure_logger` call in this process, or by a parent process),
  reuse its value; otherwise generate `datetime.now().strftime("%Y%m%dT%H%M%S")` and write it
  back to `os.environ["TTS_RUN_TIMESTAMP"]`. This is the single mechanism that makes every
  `configure_logger` call within one run -- and within any subprocess spawned by that run --
  resolve to the same log filename, per the framework's run-scoping guardrail for nested
  processes.
- `configure_logger(name, *, log_dir=None, log_level="INFO")` replaces the current `log_file`
  parameter with `log_dir`, and returns the configured, named `logging.Logger` instance:
  - `log_dir` -- whether the default or a caller-supplied path -- is created if it does not
    already exist. Default `log_dir` is `Path.cwd() / "technical_trader_solution"`.
  - The log filename is `technical_trader_solution_<TTS_RUN_TIMESTAMP>.log`, using the
    run-timestamp coordination above, so every call within one run (and its subprocesses)
    shares the same file and two concurrent runs never collide.
  - `log_level` accepts exactly `"info"`, `"debug"`, `"warning"`, `"error"` (case-insensitive,
    the complete allowed set); any other value is rejected at argument-parse time (CLI) or
    raises `ConfigurationError` (SDK/direct call), default `"info"`.
  - Continues to attach a stderr handler and a file handler, matching the existing module's
    stdout-never rule; behavior for callers that already pass no `log_file`/`log_dir` is
    unchanged apart from the new default subdirectory and datetime-stamped filename.
  - Usage contract: every entry point calls `configure_logger("technical_trader_solution", ...)`
    exactly once at startup; every other module retrieves the already-configured logger with
    `logging.getLogger("technical_trader_solution")` (a plain stdlib call, not a second
    `configure_logger` call) rather than configuring its own.
- CLI: `tts` (root `click.group` in `cli/main.py`) gains `--log-dir <dir>` and `--log-level
  [info|debug|warning|error]` options, propagated via `click.Context` (or an equivalent shared
  mechanism) to every subcommand group (`narrative`, `mcp`, `dashboard`), calling
  `configure_logger` exactly once per `tts` invocation at startup.
- SDK: `technical_trader_solution.sdk.*` functions do not call `configure_logger` themselves --
  they expect the calling process to have configured logging once already (matching the CLI and
  MCP entry-point pattern, and avoiding repeated `configure_logger` calls that would each
  re-resolve the run timestamp). For an embedding process that does not go through the CLI, the
  SDK exposes one explicit `technical_trader_solution.sdk.configure_logging(log_dir=None,
  log_level="info")` function, a thin wrapper over `configure_logger`, to be called once at
  process startup before any other SDK function.
- MCP: `tts mcp serve` (and the underlying `technical_trader_solution.mcp.server.main`) accepts
  `--log-dir`/`--log-level`, configuring the shared logger once at server startup, same pattern
  as the CLI.
- Dashboard: `tts dashboard serve` already forwards `--log-file`/`--log-level` to the `streamlit
  run` subprocess per story 001's implementation; this story renames/aligns that forwarding to
  the same `--log-dir`/`--log-level` contract, and additionally passes the parent process's
  resolved `TTS_RUN_TIMESTAMP` value through the subprocess's environment (`env=` argument to
  the `streamlit run` launch), so the dashboard subprocess's own `configure_logger` call reuses
  it via the inherited-environment-variable-first check above instead of minting a new one.
- Every command on every surface logs its own invocation at `INFO` on start, and its completion
  or failure (including the exception class name on failure) at `INFO`/`ERROR` respectively.

## Domain Exception Hierarchy

- New module: `technical_trader_solution/errors.py`, defining `TechnicalTraderSolutionError`
  (base) and narrow subclasses as needed by existing core functionality, at minimum:
  - `DataProviderError` -- the FMP data provider is unreachable or returns an unexpected
    response (raised from `core/market_data.py` and the narrative-clusters agent's `fetch.py`).
  - `InvalidClusterError` -- a requested `cluster_id` does not exist (raised from
    `sdk/narrative_clusters.py`'s `get_cluster_trend`).
  - `ConfigurationError` -- a required setting (for example `FMP_API_KEY`) is missing or
    invalid at startup.
- Each subclass carries a plain-text `message` suitable for masking and display to the human
  trader (no stack trace, no internal object repr) via `str(exc)`. The message is constructed
  with literal values, including any secret value that happens to be relevant to the failure
  (for example an unreachable URL that embeds an API key as a query parameter); masking is not
  applied at construction time. Masking is applied exactly once, when the unified error message
  (see below) is assembled for logging or display -- never at exception-construction time -- so
  a message is never double-masked and every code path that surfaces exception text goes through
  the same masking step.
- Per architecture v0.4: the core layer logs the exception class and reason
  (`logger.error("%s: %s", type(exc).__name__, exc)`) and then raises the exception; the SDK
  layer never catches
  `TechnicalTraderSolutionError` (it propagates unchanged); the CLI layer catches it at the
  command level, logs it, prints the unified error message (see below) to stderr, and exits
  `1`; the MCP layer catches it at the tool-function level and returns the unified error message
  in the tool's error response; the dashboard catches it around each SDK call and renders the
  unified error message in an `st.error(...)` banner instead of raising into the Streamlit
  process.

## Unified Error Message Format

- Template: `"{error_type}: {message}"`, where `error_type` is the exception's class name
  without the `Error` suffix (for example `DataProvider`, `InvalidCluster`,
  `Configuration`) and `message` is the exception's own message text passed through
  `mask_sensitive` (see below) at format-assembly time.
- CLI prints this string to stderr, prefixed with nothing further (click's own command name
  context is sufficient); MCP returns it as the tool response's error text; the dashboard's
  `st.error(...)` call renders the same string. All three surfaces therefore show the human
  trader the identical text for the identical failure.

## Sensitive-Data Masking

- New module-level constant in `technical_trader_solution/logging.py`:
  `MASKED_ENV_VARS = ("FMP_API_KEY", "ANTHROPIC_API_KEY")` -- an explicit, curated allowlist of
  environment-variable names known to hold secrets in this workspace's operational context, not
  a broad substring scan of all of `os.environ`. Substring/pattern matching over the full
  environment was considered and rejected: a third-party library or subprocess could set an
  unrelated variable whose name happens to contain `KEY`/`TOKEN`/etc. (a config namespace, not a
  secret), and an unbounded scan would mask that legitimate value too, hiding operational data
  the human trader needs to debug a failure. Adding a future secret (a new data provider's API
  key, for example) is a one-line addition to `MASKED_ENV_VARS`, tracked as a normal code change,
  not a spec change requirement.
- `mask_sensitive(text: str) -> str` in `technical_trader_solution/logging.py`: for each name in
  `MASKED_ENV_VARS`, if `os.environ.get(name)` is non-empty, replace every literal occurrence of
  that value in `text` with `"***MASKED***"`. Re-reads `os.environ` on every call (not cached),
  so a value set or changed after import is still covered.
- `MaskingFilter(logging.Filter)`, defined alongside `mask_sensitive`: its `filter(record)`
  method calls `record.msg = mask_sensitive(record.getMessage())` (and clears `record.args`,
  since the message is already fully rendered) before returning `True`, so every handler it is
  attached to receives an already-masked message.
- Handler and initialization-order contract: `configure_logger` creates its stderr and file
  handlers as today, attaches one shared `MaskingFilter` instance to each of those two handlers
  directly (not to the `Logger` object -- a `Filter` on a `Logger` only applies to records that
  logger itself emits, not to records a child logger propagates past it, so attaching to the
  `Logger` would miss third-party library output), and additionally attaches the same two
  handlers (each already carrying the `MaskingFilter`) to the root logger
  (`logging.getLogger()`) the first time `configure_logger` runs in a process. Every entry point
  (`cli/main.py`, `mcp/server.py`, `sdk.configure_logging`, the dashboard's Streamlit subprocess
  entry) calls `configure_logger` as its first action, before constructing any third-party
  client or server object (in particular, before constructing the MCP entry point's `FastMCP`
  server object) -- since most libraries, including FastMCP, only attach their own logging
  handlers lazily at construction time, calling `configure_logger` first guarantees the root
  logger already carries the masked handlers before any other component's log records start
  propagating to it. The same `mask_sensitive` function is called explicitly when assembling the
  unified error message (see above), so masking applies identically to log lines and
  user-facing error text via one shared implementation.

## Interface Contracts

- No change to existing command names, SDK function names, or MCP tool names; this story adds
  `--log-dir`/`--log-level` parameters and exception-based error responses to the surfaces
  defined in `docs/implementation/01-narrative-cluster-discovery-surface.md`'s Interface
  Contracts, and adds one new module (`technical_trader_solution/errors.py`) plus the masking
  additions to the existing `technical_trader_solution/logging.py`.
- `docs/implementation/01-narrative-cluster-discovery-surface.md` is not amended by this story:
  its Interface Contracts section already documents the CLI/SDK/MCP surface shape; this spec
  only adds the cross-cutting logging/error parameters and exception types layered on top,
  which apply uniformly to any current or future capability rather than being specific to
  narrative clusters.

## Validation Expectations

- Unit tests for `mask_sensitive` and the masking log filter, covering a value present in an
  error message, a value present in a log record, and the case-insensitive-name matching rule
  for future `*_KEY`/`*_TOKEN`/`*_SECRET`/`*_PASSWORD`/`*_CREDENTIAL` environment variables.
- Unit tests for `configure_logger`'s datetime-stamped filename and default `log_dir` behavior.
- CLI interface tests: a command that triggers each domain-exception subclass exits non-zero,
  prints the unified error-message format to stderr, and does not print a stack trace.
- MCP interface test: a tool call that triggers a domain exception returns the unified
  error-message format in the tool's error response, not an unhandled protocol error.
- SDK interface test: confirms `TechnicalTraderSolutionError` subclasses propagate unchanged
  from SDK functions (not swallowed or wrapped).
- Manual/demo check: the dashboard renders an `st.error(...)` banner with the unified message
  text when its underlying SDK call raises, verified by driving the dashboard with a forced
  failure (for example an invalid `cluster_id` or `FMP_API_KEY` unset).

## Dependencies

- `docs/architecture/01-technical-trader-solution.md`'s Logging and Error Handling section
  (v0.4) for the policy this spec implements.
- Existing `technical_trader_solution/logging.py`, `cli/main.py`, `cli/narrative_clusters.py`,
  `cli/dashboard.py`, `sdk/narrative_clusters.py`, `mcp/narrative_clusters.py`,
  `mcp/server.py`, `core/market_data.py`, `core/narrative_clusters/`,
  `coded_agents/narrative_clusters_agent/`, and `dashboard/discovery_surface.py`, all of which
  this story instruments in place without changing their computed outputs.

## Change Log

- v0.1 (2026-07-14) -- initial implementation specification for story 002, covering the
  extended logging contract (`--log-dir`/`--log-level`, datetime-stamped filenames), the
  domain-exception hierarchy and its per-surface handling, the unified CLI/MCP/dashboard
  error-message format, and the masked-fields list and masking technique.
- v0.2 (2026-07-14) -- implementation-spec review pass (task review-story-002-implspec-v1)
  resolved three blocking findings: added the `TTS_RUN_TIMESTAMP` inherited-environment-variable
  coordination mechanism so every `configure_logger` call within a run and its subprocesses
  shares one log file, including explicit dashboard-subprocess env propagation; specified the
  masking filter is installed on the file handler, the stderr handler, and the root logger, and
  re-scans `os.environ` on every call; clarified SDK functions do not call `configure_logger`
  internally and added an explicit `sdk.configure_logging` entry point instead. Also resolved
  three important findings (log-level validation is a closed four-value set, dashboard-subprocess
  timestamp propagation, exception-message masking happens once at format-assembly time, not at
  construction time) and the terminology-consistency findings (`Domain Exception Hierarchy`,
  `Unified Error Message Format`, unhyphenated `error message`).
- v0.3 (2026-07-14) -- implementation-spec review pass (task review-story-002-implspec-v2)
  resolved two blocking findings: replaced the unbounded `os.environ` substring scan with an
  explicit `MASKED_ENV_VARS` allowlist (`FMP_API_KEY`, `ANTHROPIC_API_KEY`) to avoid
  false-positive masking of unrelated third-party environment variables; specified that the
  `MaskingFilter` is attached to handlers (not the `Logger` object), that `configure_logger`
  also attaches its masked handlers to the root logger on first use, and that every entry point
  (including the MCP server) must call `configure_logger` before constructing any third-party
  client or server object. Also resolved three important/info findings: reworded "raises and
  logs before raising" to remove the redundant raise; documented `configure_logger`'s return
  value and the `logging.getLogger(name)` retrieval contract for non-entry-point modules; and
  specified that `log_dir` is created if missing whether default or caller-supplied.
