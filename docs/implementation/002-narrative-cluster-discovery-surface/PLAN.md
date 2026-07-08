# Implementation Plan — Narrative-Cluster Discovery Surface

## Phase 1 — Foundation

1. Confirm the data contract for narrative findings and narrative clusters.
2. Implement the core workspace models and persistence-friendly data structures.
3. Add test coverage for cluster assembly and trend metric generation.

## Phase 2 — Data ingestion

1. Add an FMP-backed ingestion adapter for earnings reports.
2. Add an FMP-backed ingestion adapter for SEC filings.
3. Add an FMP-backed ingestion adapter for news coverage.
4. Normalize source payloads into the common narrative-finding model.

## Phase 3 — Narrative extraction workflow

1. Implement an agentic extraction step that identifies storyline, topic, evidence snippet, and ticker linkage from each source item.
2. Produce candidate narrative findings with confidence and timestamp metadata.
3. Add test coverage for extraction behavior using fixture payloads.

## Phase 4 — Cluster assembly and review workflow

1. Group findings into narrative clusters using storyline and topic overlap.
2. Derive cluster-level trend metrics for mention frequency and company breadth.
3. Add a review surface that lists clusters and exposes chart-inspection actions.
4. Keep the workflow clearly framed as discovery rather than theme confirmation.

## Phase 5 — Validation

1. Run the regression tests for the workspace and clustering logic.
2. Run a workflow walkthrough with sample data.
3. Record any follow-up scope for live FMP integration and richer UI actions.
