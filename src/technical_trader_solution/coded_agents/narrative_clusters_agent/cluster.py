"""Cluster node: BERTopic topic modeling over per-ticker narrative findings, plus the
cluster-identity matching algorithm.

Per docs/implementation/01-narrative-cluster-discovery-surface.md's Storage and
Topic-Modeling Library sections: group tickers into clusters via BERTopic, then match each
new cluster against the prior run's clusters using Jaccard member-overlap (>= 0.5) AND
topic-embedding cosine similarity (>= 0.6), tie-breaking toward the higher average score
and then the older (numerically lower) cluster_id; unmatched clusters mint a new id.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date

import numpy as np
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from umap import UMAP

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    ClusterRecord,
    NarrativeFinding,
)

MIN_MEMBERS_PER_CLUSTER = 2
JACCARD_THRESHOLD = 0.5
COSINE_THRESHOLD = 0.6
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

_embedding_model: SentenceTransformer | None = None


def _get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedding_model


def _pseudo_document(ticker_findings: list[NarrativeFinding]) -> str:
    keyphrases: list[str] = []
    for finding in ticker_findings:
        keyphrases.extend(finding.keyphrases)
    # Deduplicate while preserving frequency-driven order from the extract node.
    seen: dict[str, None] = {}
    for phrase in keyphrases:
        seen.setdefault(phrase, None)
    return " ".join(seen) or "no narrative content"


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr, b_arr = np.array(a), np.array(b)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    return float(np.dot(a_arr, b_arr) / denom) if denom else 0.0


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def _match_or_create_cluster_id(
    member_tickers: list[str],
    topic_embedding: list[float],
    prior_clusters: list[ClusterRecord],
    used_prior_ids: set[str],
    next_new_id: "_ClusterIdSequence",
) -> str:
    new_members = set(member_tickers)
    candidates: list[tuple[float, str]] = []
    for prior in prior_clusters:
        if prior.cluster_id in used_prior_ids:
            continue
        jaccard = _jaccard(new_members, set(prior.member_tickers))
        cosine = _cosine_similarity(topic_embedding, prior.topic_embedding)
        if jaccard >= JACCARD_THRESHOLD and cosine >= COSINE_THRESHOLD:
            candidates.append(((jaccard + cosine) / 2, prior.cluster_id))

    if not candidates:
        return next_new_id.next()

    best_score = max(score for score, _ in candidates)
    tied = sorted(cluster_id for score, cluster_id in candidates if score == best_score)
    return tied[0]  # numerically-lower / older cluster_id wins ties


class _ClusterIdSequence:
    """Assigns new cluster_id values as cluster-0001, cluster-0002, ... continuing from
    the highest existing numeric suffix, so "older" ids sort numerically lower."""

    def __init__(self, existing_cluster_ids: list[str]) -> None:
        existing_numbers = [
            int(cid.split("-")[-1])
            for cid in existing_cluster_ids
            if cid.startswith("cluster-") and cid.split("-")[-1].isdigit()
        ]
        self._next = (max(existing_numbers) + 1) if existing_numbers else 1

    def next(self) -> str:
        cluster_id = f"cluster-{self._next:04d}"
        self._next += 1
        return cluster_id


def build_clusters(
    findings: list[NarrativeFinding],
    run_date: date,
    prior_clusters: list[ClusterRecord],
    all_known_cluster_ids: list[str],
) -> list[ClusterRecord]:
    """Group this run's findings' tickers into clusters and resolve cluster identity."""

    findings_by_ticker: dict[str, list[NarrativeFinding]] = defaultdict(list)
    for finding in findings:
        findings_by_ticker[finding.ticker].append(finding)

    tickers = sorted(findings_by_ticker)
    if len(tickers) < MIN_MEMBERS_PER_CLUSTER:
        return []

    docs = [_pseudo_document(findings_by_ticker[ticker]) for ticker in tickers]
    embeddings = _get_embedding_model().encode(docs, show_progress_bar=False)

    # UMAP's default n_neighbors (15) errors out below that many samples; scale it down for
    # small nightly universes (including this module's own small test fixtures) instead of
    # requiring a fixed minimum universe size.
    umap_model = UMAP(
        n_neighbors=min(15, max(2, len(docs) - 1)),
        n_components=min(5, max(2, len(docs) - 2)),
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )
    hdbscan_model = HDBSCAN(
        min_cluster_size=MIN_MEMBERS_PER_CLUSTER,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )
    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        min_topic_size=MIN_MEMBERS_PER_CLUSTER,
        calculate_probabilities=False,
    )
    topics, _ = topic_model.fit_transform(docs, embeddings=embeddings)

    tickers_by_topic: dict[int, list[str]] = defaultdict(list)
    embedding_indices_by_topic: dict[int, list[int]] = defaultdict(list)
    for index, topic_id in enumerate(topics):
        if topic_id == -1:
            continue  # BERTopic outlier: no shared/adjacent narrative found this run.
        tickers_by_topic[topic_id].append(tickers[index])
        embedding_indices_by_topic[topic_id].append(index)

    id_sequence = _ClusterIdSequence(all_known_cluster_ids)
    used_prior_ids: set[str] = set()
    clusters: list[ClusterRecord] = []

    for topic_id, member_tickers in tickers_by_topic.items():
        topic_embedding = np.mean(
            [embeddings[i] for i in embedding_indices_by_topic[topic_id]], axis=0
        ).tolist()
        frequency_of_mention = sum(len(findings_by_ticker[ticker]) for ticker in member_tickers)
        cluster_id = _match_or_create_cluster_id(
            member_tickers, topic_embedding, prior_clusters, used_prior_ids, id_sequence
        )
        used_prior_ids.add(cluster_id)

        top_words = [word for word, _ in topic_model.get_topic(topic_id)[:5]]
        clusters.append(
            ClusterRecord(
                cluster_id=cluster_id,
                run_date=run_date,
                topic_label=", ".join(top_words) or "unlabeled",
                member_tickers=sorted(member_tickers),
                frequency_of_mention=frequency_of_mention,
                company_breadth=len(member_tickers),
                topic_embedding=topic_embedding,
            )
        )

    return clusters
