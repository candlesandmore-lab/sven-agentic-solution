"""SQLite storage for narrative findings, clusters, and trend snapshots.

Per docs/implementation/01-narrative-cluster-discovery-surface.md's Storage section:
tables narrative_findings, clusters, cluster_trend_snapshots, indexed by ticker and
run_date. This is the only module that reads or writes the store directly -- the SDK,
CLI, MCP, and Discovery Surface all go through the SDK functions built on top of it, per
the Discovery Surface's SDK-only data-access contract.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime
from pathlib import Path

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    ClusterRecord,
    ClusterTrendSnapshot,
    NarrativeFinding,
    SourceType,
)

DEFAULT_DB_PATH = Path("data/narrative_clusters.sqlite")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS narrative_findings (
    ticker TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    published_at TEXT NOT NULL,
    keyphrases TEXT NOT NULL,
    entities TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    run_date TEXT NOT NULL,
    PRIMARY KEY (source_type, source_id)
);
CREATE INDEX IF NOT EXISTS idx_narrative_findings_ticker ON narrative_findings (ticker);
CREATE INDEX IF NOT EXISTS idx_narrative_findings_run_date ON narrative_findings (run_date);

CREATE TABLE IF NOT EXISTS clusters (
    cluster_id TEXT NOT NULL,
    run_date TEXT NOT NULL,
    topic_label TEXT NOT NULL,
    member_tickers TEXT NOT NULL,
    frequency_of_mention INTEGER NOT NULL,
    company_breadth INTEGER NOT NULL,
    topic_embedding TEXT NOT NULL,
    PRIMARY KEY (cluster_id, run_date)
);
CREATE INDEX IF NOT EXISTS idx_clusters_run_date ON clusters (run_date);

CREATE TABLE IF NOT EXISTS cluster_trend_snapshots (
    cluster_id TEXT NOT NULL,
    run_date TEXT NOT NULL,
    frequency_of_mention INTEGER NOT NULL,
    company_breadth INTEGER NOT NULL,
    PRIMARY KEY (cluster_id, run_date)
);
CREATE INDEX IF NOT EXISTS idx_trend_cluster_id ON cluster_trend_snapshots (cluster_id);
"""


class NarrativeClustersStore:
    """Owns the narrative_clusters SQLite database."""

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    # -- Narrative findings --------------------------------------------------------

    def save_findings(self, findings: list[NarrativeFinding], run_date: date) -> None:
        with self._connect() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO narrative_findings "
                "(ticker, source_type, source_id, published_at, keyphrases, entities, "
                "fetched_at, run_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        f.ticker,
                        f.source_type.value,
                        f.source_id,
                        f.published_at.isoformat(),
                        json.dumps(f.keyphrases),
                        json.dumps(f.entities),
                        f.fetched_at.isoformat(),
                        run_date.isoformat(),
                    )
                    for f in findings
                ],
            )

    def get_findings_for_run(self, run_date: date) -> list[NarrativeFinding]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT ticker, source_type, source_id, published_at, keyphrases, entities, "
                "fetched_at FROM narrative_findings WHERE run_date = ?",
                (run_date.isoformat(),),
            ).fetchall()
        return [
            NarrativeFinding(
                ticker=row[0],
                source_type=SourceType(row[1]),
                source_id=row[2],
                published_at=datetime.fromisoformat(row[3]),
                keyphrases=json.loads(row[4]),
                entities=json.loads(row[5]),
                fetched_at=datetime.fromisoformat(row[6]),
            )
            for row in rows
        ]

    def latest_watermark(self, ticker: str) -> datetime | None:
        """Most recent `published_at` already stored for `ticker`, across all runs."""

        with self._connect() as conn:
            row = conn.execute(
                "SELECT MAX(published_at) FROM narrative_findings WHERE ticker = ?", (ticker,)
            ).fetchone()
        return datetime.fromisoformat(row[0]) if row and row[0] else None

    # -- Clusters --------------------------------------------------------------------

    def save_clusters(self, clusters: list[ClusterRecord]) -> None:
        with self._connect() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO clusters (cluster_id, run_date, topic_label, "
                "member_tickers, frequency_of_mention, company_breadth, topic_embedding) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        c.cluster_id,
                        c.run_date.isoformat(),
                        c.topic_label,
                        json.dumps(c.member_tickers),
                        c.frequency_of_mention,
                        c.company_breadth,
                        json.dumps(c.topic_embedding),
                    )
                    for c in clusters
                ],
            )

    def get_clusters(self, run_date: date | None = None) -> list[ClusterRecord]:
        with self._connect() as conn:
            if run_date is not None:
                rows = conn.execute(
                    "SELECT cluster_id, run_date, topic_label, member_tickers, "
                    "frequency_of_mention, company_breadth, topic_embedding FROM clusters "
                    "WHERE run_date = ?",
                    (run_date.isoformat(),),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT cluster_id, run_date, topic_label, member_tickers, "
                    "frequency_of_mention, company_breadth, topic_embedding FROM clusters "
                    "WHERE run_date = (SELECT MAX(run_date) FROM clusters)"
                ).fetchall()
        return [
            ClusterRecord(
                cluster_id=row[0],
                run_date=date.fromisoformat(row[1]),
                topic_label=row[2],
                member_tickers=json.loads(row[3]),
                frequency_of_mention=row[4],
                company_breadth=row[5],
                topic_embedding=json.loads(row[6]),
            )
            for row in rows
        ]

    def all_cluster_ids(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT DISTINCT cluster_id FROM clusters").fetchall()
        return [row[0] for row in rows]

    def get_prior_run_clusters(self, before: date) -> list[ClusterRecord]:
        """Clusters from the most recent run strictly before `before`, for identity matching."""

        with self._connect() as conn:
            row = conn.execute(
                "SELECT MAX(run_date) FROM clusters WHERE run_date < ?", (before.isoformat(),)
            ).fetchone()
        prior_run_date = date.fromisoformat(row[0]) if row and row[0] else None
        return self.get_clusters(prior_run_date) if prior_run_date else []

    # -- Trend snapshots ---------------------------------------------------------------

    def save_trend_snapshots(self, snapshots: list[ClusterTrendSnapshot]) -> None:
        with self._connect() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO cluster_trend_snapshots "
                "(cluster_id, run_date, frequency_of_mention, company_breadth) "
                "VALUES (?, ?, ?, ?)",
                [
                    (s.cluster_id, s.run_date.isoformat(), s.frequency_of_mention, s.company_breadth)
                    for s in snapshots
                ],
            )

    def get_cluster_trend(self, cluster_id: str) -> list[ClusterTrendSnapshot]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT cluster_id, run_date, frequency_of_mention, company_breadth "
                "FROM cluster_trend_snapshots WHERE cluster_id = ? ORDER BY run_date",
                (cluster_id,),
            ).fetchall()
        return [
            ClusterTrendSnapshot(
                cluster_id=row[0],
                run_date=date.fromisoformat(row[1]),
                frequency_of_mention=row[2],
                company_breadth=row[3],
            )
            for row in rows
        ]
