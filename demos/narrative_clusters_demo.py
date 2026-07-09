"""Demo: narrative-cluster discovery end to end, into a dashboard-ready store.

Runs the Narrative Extraction and Clustering Pipeline against
tests/fixtures/narrative_clusters/documents.yaml (standing in for a nightly FMP fetch),
prints the resulting cluster(s) with topic label and trend snapshot, and prints the
`tts dashboard serve` command to inspect the result -- including a working
chart-inspection link -- in the Discovery Surface page.

Requires ANTHROPIC_API_KEY (the label node's one bounded model call per cluster); prints
a clear message and exits without crashing if it is not configured.

Run with:
    uv run python demos/narrative_clusters_demo.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import yaml

from technical_trader_solution.coded_agents.narrative_clusters_agent.agent import (
    NarrativeClustersAgent,
)
from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    RawDocument,
    SourceType,
)

FIXTURE_PATH = Path("tests/fixtures/narrative_clusters/documents.yaml")
DEMO_DB_PATH = Path("data/demo_narrative_clusters.sqlite")
DEMO_RUN_DATE = "2026-06-06"


def _load_documents() -> list[RawDocument]:
    raw = yaml.safe_load(FIXTURE_PATH.read_text())
    return [
        RawDocument(
            ticker=entry["ticker"],
            source_type=SourceType(entry["source_type"]),
            source_id=entry["source_id"],
            published_at=datetime.fromisoformat(entry["published_at"]),
            text=entry["text"],
        )
        for entry in raw["documents"]
    ]


def main() -> None:
    import os

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not configured; the label node needs it. Skipping demo.")
        return

    documents = _load_documents()
    tickers = sorted({doc.ticker for doc in documents})

    def fixture_fetch_documents(ticker: str, since):
        return [doc for doc in documents if doc.ticker == ticker]

    DEMO_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    agent = NarrativeClustersAgent(db_path=DEMO_DB_PATH)

    result = agent.run(
        task_id=f"demo-{DEMO_RUN_DATE}",
        inputs={
            "run_date": DEMO_RUN_DATE,
            "tickers": tickers,
            "fetch_documents": fixture_fetch_documents,
        },
    )

    if result["status"] != "succeeded":
        print(f"Demo run did not succeed: {result}")
        sys.exit(1)

    clusters = result["output"]["clusters"]
    print(f"Run date {result['output']['run_date']}: {len(clusters)} cluster(s) found.\n")

    for cluster in clusters:
        print(f"Cluster {cluster['cluster_id']}: {cluster['topic_label']}")
        print(f"  Members: {', '.join(cluster['member_tickers'])}")
        print(
            f"  Frequency of mention: {cluster['frequency_of_mention']}  "
            f"Company breadth: {cluster['company_breadth']}"
        )
        trend = agent.store.get_cluster_trend(cluster["cluster_id"])
        print(f"  Trend snapshots ({len(trend)}):")
        for snapshot in trend:
            print(
                f"    {snapshot.run_date}: frequency={snapshot.frequency_of_mention} "
                f"breadth={snapshot.company_breadth}"
            )
        print()

    print("Inspect this run in the Discovery Surface dashboard:")
    print(f"  uv run tts dashboard serve --db-path {DEMO_DB_PATH}")
    if clusters:
        print(
            f'  Then click "Inspect charts" on the "{clusters[0]["topic_label"]}" cluster '
            f"to see {', '.join(clusters[0]['member_tickers'])} side by side."
        )


if __name__ == "__main__":
    main()
