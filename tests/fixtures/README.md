# Test fixtures

User-editable, data-driven fixture files live here, one subdirectory per capability (for
example `narrative_clusters/`). Tests read their input from these fixture files rather than
hard-coding capability-specific sample data in test modules, and skip (not fail) when a
required fixture or credential is missing.

- `narrative_clusters/documents.yaml` — sample earnings-transcript, SEC-filing, and news
  documents used by story 001's extraction, clustering, and trend tests (added by
  `task_5_qa_validation`; see
  `docs/implementation/01-narrative-cluster-discovery-surface.md`).
- `narrative_clusters/prior_run_clusters.yaml` — a sample prior-run cluster set used to
  exercise the cluster-identity matching algorithm's Jaccard/cosine thresholds (added by
  `task_5_qa_validation`).
