# Narrative-Cluster Discovery Surface Implementation Specification

## Purpose

Define the implementation contract for story 001 (US-015 Narrative-Cluster Discovery Surface):
the nightly narrative extraction and clustering pipeline, its local store, and the Discovery
Surface page of the Technical Trader Solution's local web dashboard (see
`docs/architecture/01-technical-trader-solution.md`, Delivery Interface).

## Scope

### In scope

- Nightly data ingestion from the FMP data provider (earnings call transcripts, SEC filings,
  news coverage) for every ticker in the eligible universe.
- Per-ticker narrative/topic extraction, topic modeling, cluster formation, cluster labeling,
  and frequency/breadth trend computation.
- Local storage of narrative findings, clusters, and trend snapshots.
- The Discovery Surface page: cluster list with topic label and trend, and navigation into a
  side-by-side chart view of a cluster's member tickers.

### Out of scope

- Theme creation and theme maintenance (a human trader action, out of this capability's scope
  per STR-011; covered by future stories).
- Bond network, sync rank, and pair-bond computation (separate, not-yet-scheduled stories).
- Any capability beyond the Discovery Surface page inside the local web dashboard shell (the
  dashboard shell itself is introduced here only to the extent story 001 needs it to render one
  page; further dashboard-wide navigation/shell work is a follow-up story if more pages are
  added later).

## Role

- Name: Narrative Extraction and Clustering Pipeline.
- Type: coded agent (LangGraph, ClaudeCode SDK base), per
  `docs/architecture/01-technical-trader-solution.md` Solution-Surface Classification.
- Primary goal: turn raw FMP text sources into per-ticker narrative findings and labeled ticker
  clusters, refreshed nightly, without requiring open-ended reasoning or tool choice.

## Coded-Agent Flow

- Entry node: load the nightly run's eligible-universe ticker list and prior run's watermark
  (last-seen document timestamp per ticker/source) so only new documents are processed.
- Fetch node: call the FMP data provider for each ticker's earnings call transcripts, SEC
  filings, and news items published since the watermark.
- Extract node: derive per-document narrative/topic signals (keyphrase and named-entity
  extraction) from each fetched document, producing one narrative-finding record per document.
- Cluster node: run topic modeling across the current run's narrative findings for the full
  eligible universe, grouping tickers whose dominant topics are shared or overlapping
  (independent of pair-bond, sync, or theme status).
- Label node: for each resulting cluster, issue one bounded model call that turns the cluster's
  top keyphrases and a small sample of representative excerpts into a short topic label.
- Trend node: compute each cluster's frequency-of-mention (finding count) and company-breadth
  (distinct ticker count) for the run, and append a trend snapshot.
- Persist node: write narrative findings, cluster assignments, cluster labels, and trend
  snapshots to the local store.
- Evaluate node: validate the run's output against the schema below (non-empty findings when
  source documents existed, every cluster has a label and at least one member, trend snapshot
  recorded); refine (re-run label or cluster node) on failure, per the coded-agent runtime
  contract.
- Terminal node: mark the run complete, or return the five-iteration failure contract with
  questions if evaluation cannot pass.

## Data Contracts

### Narrative finding record

| Field | Type | Notes |
| --- | --- | --- |
| `ticker` | string | Eligible-universe ticker this finding belongs to. |
| `source_type` | enum | `earnings_transcript`, `sec_filing`, or `news`. |
| `source_id` | string | FMP-provided identifier for the source document. |
| `published_at` | datetime | Source document's publication timestamp. |
| `keyphrases` | list of strings | Extracted keyphrases from the document. |
| `entities` | list of strings | Extracted named entities from the document. |
| `fetched_at` | datetime | When this workspace fetched the document. |

### Cluster record

| Field | Type | Notes |
| --- | --- | --- |
| `cluster_id` | string | Stable id for the cluster across nightly runs while membership persists. |
| `run_date` | date | Nightly run this cluster snapshot belongs to. |
| `topic_label` | string | Short topic label or summary produced by the label node. |
| `member_tickers` | list of strings | Tickers assigned to this cluster for this run. |
| `frequency_of_mention` | integer | Narrative-finding count feeding this cluster for this run. |
| `company_breadth` | integer | Distinct member-ticker count for this run. |

### Cluster trend snapshot

| Field | Type | Notes |
| --- | --- | --- |
| `cluster_id` | string | References the cluster record. |
| `run_date` | date | Nightly run date. |
| `frequency_of_mention` | integer | Same-run value, retained for trend charting over time. |
| `company_breadth` | integer | Same-run value, retained for trend charting over time. |

## Storage

- Local SQLite store (`data/narrative_clusters.sqlite`), matching this workspace's existing
  coded-agent-state persistence pattern (`.agent_building_agent/coded_agent_state/*.sqlite`).
- Tables: `narrative_findings`, `clusters`, `cluster_trend_snapshots`, indexed by `ticker` and
  `run_date` for nightly incremental writes and Discovery Surface reads.
- Cluster identity persists across nightly runs by matching each new run's cluster against the
  prior run's clusters:
  1. Compute the Jaccard similarity of `member_tickers` between the new cluster and each prior
     cluster (intersection over union of the two ticker sets).
  2. Compute the cosine similarity of the two clusters' topic embeddings (the topic-modeling
     library's own topic-vector representation, not the per-document embeddings).
  3. A new cluster matches a prior cluster when both `Jaccard >= 0.5` (a majority of member
     tickers are shared) and `cosine similarity >= 0.6` (the topic itself is stable, not just an
     incidental ticker overlap).
  4. If more than one prior cluster satisfies both thresholds, match to the one with the higher
     average of the two scores; ties break toward the prior cluster with the older (numerically
     lower) `cluster_id`, favoring identity stability over recency.
  5. If no prior cluster satisfies both thresholds, mint a new `cluster_id` for the new cluster.
  These thresholds are a starting point, not a corpus-derived constant; they may be tuned during
  implementation execution based on fixture and demo behavior, recorded as a task-plan or QA
  finding rather than silently changed.
- Coded-agent task-id state (for the refine/evaluator loop, not the nightly data itself) is
  co-located with the data store at `<db_path's directory>/narrative-clusters-agent-state.sqlite`,
  not a workspace-global path, so two agents pointed at different `db_path` values (for example
  separate test runs) never share or collide on persisted task state.

## Topic-Modeling Library

- Chosen: BERTopic. It combines document embeddings, clustering, and per-topic keyphrase
  extraction in one library, which the label node's bounded model call and the cluster-identity
  matching algorithm above both depend on (BERTopic's topic vectors are the "topic embeddings"
  used for cosine similarity in matching).
- Alternatives considered: (1) classic LDA -- rejected, requires manually fixing the topic count
  in advance and produces weaker semantic (embedding-based) similarity for judging adjacent
  narratives; (2) scikit-learn NMF -- rejected for the same reasons as LDA, plus less built-in
  tooling for a corpus that grows incrementally every night.
- This is a non-UI implementation choice; it does not change what the human trader sees or does,
  only how the pipeline derives clusters internally.

## Discovery Surface (Dashboard Page)

- Framework: Streamlit, chosen over a custom API-plus-frontend build or Dash for fastest delivery
  of an interactive, Python-native page reusing the pipeline's own data-access functions
  directly; Plotly for the trend and side-by-side chart rendering embedded in the page.
- Data access: the page calls only the `narrative_clusters` SDK functions (`get_clusters`,
  `get_cluster_trend`) for all data it displays; it never queries the SQLite store directly, so
  the SDK layer stays the single, tested data-access path shared by the CLI, the dashboard, and
  any future MCP caller.
- Page contents: a list of current clusters, each showing its `topic_label`, current
  `frequency_of_mention` and `company_breadth`, and a trend sparkline from
  `cluster_trend_snapshots`.
- Selecting a cluster opens a side-by-side chart view of its `member_tickers`, sourced from the
  FMP data provider's historical price endpoint (the same data provider already approved for
  this story; no new external dependency).
- Theme creation is never offered as an automated action from this page; the page only supports
  chart inspection, per STR-011 and the story's success criteria.

## Interface Contracts

Per the mandatory SDK/CLI/MCP generation rule for a shared core Python layer:

- Core Python layer: `narrative_clusters` package (`technical_trader_solution.coded_agents.
  narrative_clusters_agent`) exposing `run_nightly_pipeline(tickers, run_date=None)`,
  `get_clusters(run_date=None)`, and `get_cluster_trend(cluster_id)` from
  `technical_trader_solution.sdk.narrative_clusters`. All three return or accept
  `ClusterView` (or its plain-dict dump), never the internal `ClusterRecord` -- see
  Trader-Facing View below.
- CLI command-line entry point: `tts` (Technical Trader Solution) -- the canonical short name
  for this workspace's own CLI, distinct from `agent-building-agent`'s own CLI. Introduced here
  because story 001 is the first capability to need one; later stories reuse `tts` rather than
  inventing a new prefix.
- SDK: `technical_trader_solution.sdk.narrative_clusters` re-exports the core functions.
  Status: generated.
- CLI: `tts narrative run-nightly`, `tts narrative show-clusters`, `tts narrative show-trend
  <cluster_id>` (read commands added in task_3 to keep CLI/SDK/MCP aligned per the
  interface-rules sub-skill), and `tts mcp serve` (launches this workspace's own MCP server).
  `tts dashboard serve` is task_4's addition. Status: generated.
- MCP: `narrative_run_nightly_pipeline`, `narrative_get_clusters`, `narrative_get_cluster_trend`
  tools registered on this workspace's own FastMCP server
  (`technical_trader_solution.mcp.server`, launched via `tts mcp serve`) and registered in
  this workspace's `.mcp.json` alongside `agent-building-agent`'s own server entry, so the
  human trader (or a future local orchestrator) can call them from this machine. Status:
  generated. This is registration within this workspace's own local tooling, not the separate
  "distributable instructed-agent asset" packaging concept (rendering agent.md/SKILL.md
  assets into other developers' vs-code-ghcp/vs-code-claude/cli-cline workspaces) -- the
  Technical Trader Solution is not being packaged for redistribution to other developers in
  story 001, so INSTALL.md and framework-target rendering do not apply here; only this
  workspace's own local MCP registration does, and it is required, not optional.
- Prompt contract (label node): input is a cluster's top keyphrases plus up to three
  representative excerpts; output is exactly one short topic label string (no JSON wrapper
  needed since the label node's output is a single string, unlike the four framework coded
  agents' structured JSON payloads).

### Coded-agent runtime configuration correction (task_3)

The implementation spec originally said the coded agent would be "registered as a new
section in this workspace's `coded-agent-config.yaml`" -- that file is
`agent-building-agent`'s own runtime configuration, and its loader validates `coded_agents`
keys against a closed set of its four framework agents (story-telling-agent,
review-validation-agent, instructed-agent-creation-agent, qa-agent); it cannot and should
not be extended with a deliverable's own coded agents. Corrected in task_3: a new,
separate `tts-coded-agent-config.yaml` at the workspace root (loaded by
`technical_trader_solution.coded_agents.config`) carries the same shape -- one YAML file, a
section per Technical Trader Solution coded agent, LLM endpoint + model + user-reviewable
system prompt -- for the same reason that pattern exists (a trader can change model or
prompt without touching code), scoped correctly to this deliverable. Absence of the file,
or of a given agent's section in it, is not an error: every coded agent falls back to its
own hardcoded default model and system prompt.

### Trader-Facing View

Per the task_2 review checkpoint's deferred finding: `ClusterRecord.topic_embedding` (the
internal matching-algorithm field) must never reach a consumer outside the coded agent
itself. `ClusterView` (same fields as `ClusterRecord` minus `topic_embedding`) is what the
coded agent's own run output, the SDK, the CLI, and the MCP tools all return; the full
`ClusterRecord` (with embedding) is persisted to storage for the next run's identity
matching and never leaves it.

## Validation Expectations

- Unit tests for extraction, clustering, and trend computation using data-driven fixtures under
  `tests/fixtures/narrative_clusters/`: `documents.yaml` (a small sample set of
  earnings-transcript, SEC-filing, and news documents covering at least two distinct narrative
  topics across multiple tickers, each entry carrying `ticker`, `source_type`, `source_id`,
  `published_at`, and raw text) and `prior_run_clusters.yaml` (a sample prior-run cluster set
  used to exercise the cluster-identity matching algorithm's Jaccard/cosine thresholds). Unit
  tests read these fixture files rather than hard-coding sample text in test modules.
- Interface tests for the CLI, SDK, and MCP surfaces, reusing the same fixture files as live
  input when an FMP API key is configured, and as mocked responses otherwise.
- Prompt-validation test for the label node (developer approval required, per the QA agent's
  prompt-flow check requirement), confirming the evaluate node correctly validates the label
  node's single-string output (non-empty, bounded length) and triggers refinement when the
  output is missing or malformed, since this output shape differs from the structured JSON
  payloads the four framework coded agents produce.
- Demo: a run against fixture data showing at least one multi-ticker cluster, its topic label,
  its trend snapshot, and the Discovery Surface page rendering that cluster with a working
  chart-inspection link.

## Dependencies

- FMP data provider API access (existing) for earnings call transcripts, SEC filings, news, and
  historical price data. FMP's approval as this workspace's data provider is recorded in
  `docs/architecture/01-technical-trader-solution.md`'s Non-Functional Constraints section;
  this spec's use of the historical price endpoint is the same already-approved provider, not
  a new external dependency.
- Topic-modeling and embedding libraries for the cluster node; the specific package choice is
  deferred to the task plan because it affects only the internal clustering and cluster-matching
  implementation (see Storage above), not the interface contracts or storage schema already
  defined here.
- Streamlit and Plotly for the Discovery Surface page.
- Depends on `docs/architecture/01-technical-trader-solution.md`'s Delivery Interface and
  Solution-Surface Classification decisions.

## Change Log

- v0.1 (2026-07-08) -- initial implementation specification for story 001, covering the nightly
  narrative extraction and clustering pipeline, its local store, and the Discovery Surface
  dashboard page.
- v0.2 (2026-07-08) -- implementation-spec review pass (task
  review-us-015-implementation-spec-v1): explicitly deferred the cluster-identity matching
  algorithm to the task plan (Storage section); added the label node's single-string output
  validation expectation (Validation Expectations); cross-referenced FMP historical-price-data
  approval and clarified the topic-modeling library deferral rationale (Dependencies).
- v0.3 (2026-07-08) -- task-plan review pass (task review-us-015-task-plan-v1) found the v0.2
  deferral of the matching algorithm and library choice to task execution itself violated
  abstraction alignment. Resolved directly in this spec instead of at task-execution time: added
  the concrete Jaccard/cosine cluster-matching algorithm and thresholds (Storage section), chose
  BERTopic as the topic-modeling library with alternatives considered (new Topic-Modeling
  Library section), named the workspace's CLI entry point `tts` and clarified MCP registration is
  local-workspace tooling, not distributable-asset packaging (Interface Contracts), specified the
  dashboard's SDK-only data-access contract (Discovery Surface), and added concrete fixture file
  paths (Validation Expectations).
- v0.4 (2026-07-09) -- task_3 (invocation-surface wiring): corrected the coded-agent runtime
  configuration mechanism from a `coded-agent-config.yaml` section (that file is scoped to
  `agent-building-agent`'s own four framework agents and cannot be extended) to a new, separate
  `tts-coded-agent-config.yaml` (Interface Contracts); added the `ClusterView` trader-facing model
  excluding `topic_embedding` from every SDK/CLI/MCP response, resolving the task_2 review
  checkpoint's deferred finding (new Trader-Facing View section); added `tts narrative
  show-clusters`/`show-trend` read commands and `tts mcp serve` for CLI/SDK/MCP alignment
  (Interface Contracts); fixed a state-isolation bug found during interface testing where
  task-id state defaulted to a workspace-global path instead of one co-located with `db_path`,
  causing an unrelated prior run's state to be resumed (Storage section).
