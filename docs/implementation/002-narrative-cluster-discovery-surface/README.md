# Implementation Spec — Narrative-Cluster Discovery Surface

## Scope

Deliver the first implementation slice for the narrative-cluster discovery surface.

## Implementation objectives

- Establish an agentic workflow that extracts narrative findings from earnings reports, SEC filings, and news coverage through the FMP data provider.
- Persist narrative clusters and their supporting metadata for review.
- Enable the human trader to inspect a cluster and launch side-by-side chart review for its members.
- Keep the experience clearly framed as discovery rather than automated theme confirmation.

## Proposed implementation steps

1. Create ingestion adapters for FMP earnings, SEC filing, and news data.
2. Implement a narrative extraction workflow that produces candidate narrative findings with ticker linkage.
3. Add a clustering service that groups findings into narrative clusters using storyline and topic overlap.
4. Create a persisted workspace model for clusters, members, and trend metrics.
5. Add the review surface that lists clusters and exposes chart-inspection actions.
6. Validate the flow with a representative sample of source data and a walkthrough of the trader workflow.

## Suggested component boundaries

- Data provider adapters
- Narrative extraction workflow
- Cluster assembly service
- Workspace persistence layer
- Review UI or workspace view

## Current implementation detail

The first implementation slice currently provides the core workspace abstraction and clustering behavior in [src/sven_agentic_solution/narrative_cluster_workspace.py](src/sven_agentic_solution/narrative_cluster_workspace.py). It includes:

- a narrative finding model for extracted evidence
- a narrative cluster model for persisted review state
- a workspace class that ingests findings, clusters them by storyline and topic, and computes basic trend metrics

The next implementation step is to add the FMP ingestion adapters and the agentic extraction stage that populate these models from live data.

## Acceptance notes

The first slice is considered complete when the trader can review a cluster generated from FMP-backed narrative findings and transition into chart inspection without implying that the cluster is already a theme.
