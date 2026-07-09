"""Data contracts for the Narrative Extraction and Clustering Pipeline.

Field names and semantics match
docs/implementation/01-narrative-cluster-discovery-surface.md's Data Contracts section.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class SourceType(str, Enum):
    EARNINGS_TRANSCRIPT = "earnings_transcript"
    SEC_FILING = "sec_filing"
    NEWS = "news"


class RawDocument(BaseModel):
    """One fetched source document, before extraction."""

    ticker: str
    source_type: SourceType
    source_id: str
    published_at: datetime
    text: str


class NarrativeFinding(BaseModel):
    """One extracted narrative finding, per document."""

    ticker: str
    source_type: SourceType
    source_id: str
    published_at: datetime
    keyphrases: list[str]
    entities: list[str]
    fetched_at: datetime


class ClusterRecord(BaseModel):
    """One cluster's snapshot for a single nightly run."""

    cluster_id: str
    run_date: date
    topic_label: str
    member_tickers: list[str]
    frequency_of_mention: int
    company_breadth: int
    topic_embedding: list[float]
    """BERTopic's topic-vector representation, used by the cluster-identity matching
    algorithm's cosine-similarity step. Not surfaced to the human trader."""


class ClusterTrendSnapshot(BaseModel):
    """One cluster's trend datapoint, retained across runs for charting."""

    cluster_id: str
    run_date: date
    frequency_of_mention: int
    company_breadth: int


class ClusterView(BaseModel):
    """Trader-facing view of a cluster: `ClusterRecord` without `topic_embedding`.

    Per the task_2 review checkpoint's deferred finding, the SDK, CLI, MCP, and Discovery
    Surface all expose this view, never the raw `ClusterRecord` -- the topic embedding is
    an internal cluster-identity-matching detail, not trader-facing information.
    """

    cluster_id: str
    run_date: date
    topic_label: str
    member_tickers: list[str]
    frequency_of_mention: int
    company_breadth: int

    @classmethod
    def from_record(cls, record: ClusterRecord) -> "ClusterView":
        return cls(
            cluster_id=record.cluster_id,
            run_date=record.run_date,
            topic_label=record.topic_label,
            member_tickers=record.member_tickers,
            frequency_of_mention=record.frequency_of_mention,
            company_breadth=record.company_breadth,
        )
