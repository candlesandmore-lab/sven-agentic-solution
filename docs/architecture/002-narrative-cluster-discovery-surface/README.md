# Architecture — Narrative-Cluster Discovery Surface

## Summary

This story introduces a stateful narrative-cluster workspace that lets the human trader review narrative findings extracted from earnings reports, SEC filings, and news coverage, group them into narrative clusters, and inspect the underlying charts before deciding whether to create a theme.

## Architectural direction

The first delivery uses a dedicated workspace for narrative clusters with persisted records for:

- narrative clusters
- cluster members and linked tickers
- storyline and topic metadata
- trend indicators for mention frequency and company breadth
- actions that launch chart inspection for a cluster

## Key components

1. Ingestion layer
   - Pulls source content from the FMP data provider for earnings reports, SEC filings, and news coverage.
   - Normalizes the payloads into a common representation for narrative extraction.

2. Narrative extraction workflow
   - Uses an agentic workflow to identify storylines, topics, and evidence snippets from each source.
   - Produces candidate narrative findings with ticker associations and trend signals.

3. Cluster assembly service
   - Groups narrative findings into narrative clusters based on shared or adjacent storyline and topic overlap.
   - Tracks cluster-level metrics such as mention frequency and company breadth.

4. Workspace presentation layer
   - Renders the narrative-cluster workspace so the human trader can review clusters and transition to chart inspection.
   - Keeps the surface clearly separate from theme confirmation.

## Data model sketch

- Narrative finding
  - source_type
  - source_id
  - ticker
  - storyline
  - topic
  - evidence_excerpt
  - mention_timestamp
  - confidence

- Narrative cluster
  - cluster_id
  - storyline
  - topic_summary
  - member_tickers
  - trend_metrics
  - created_at
  - updated_at

## Implementation detail map

The current implementation slice is intentionally focused on the workspace and clustering core:

- Ingestion layer: the structure is defined in the workspace model and is ready to be extended with FMP-specific adapters for earnings reports, SEC filings, and news coverage.
- Narrative extraction workflow: the current code does not yet call a live provider or an external agent, but the data model is prepared to carry extracted findings once that workflow is wired in.
- Cluster assembly service: this is implemented in [src/sven_agentic_solution/narrative_cluster_workspace.py](src/sven_agentic_solution/narrative_cluster_workspace.py) through the clustering logic that groups findings by storyline and topic and derives trend metrics.
- Workspace presentation layer: the stateful workspace abstraction is implemented in [src/sven_agentic_solution/narrative_cluster_workspace.py](src/sven_agentic_solution/narrative_cluster_workspace.py), and the regression coverage lives in [tests/test_narrative_cluster_workspace.py](tests/test_narrative_cluster_workspace.py).

## Notes

This architecture favors a persistent workspace over a one-off view so the workflow can evolve beyond initial discovery into richer review and follow-up actions.
