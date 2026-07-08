"""Per-document keyphrase and named-entity extraction (extract node).

Deliberately dependency-light: frequency-based keyphrase extraction over stopword-filtered
unigrams/bigrams, and a capitalized-sequence heuristic for entities, rather than adding a
second heavy NLP model alongside BERTopic's own embedding model. This is a documented
implementation choice, not a claim of production-grade NLP; it feeds the cluster node's
topic modeling (which does the semantic heavy lifting via document embeddings) and the
label node's representative-excerpt selection, not a standalone information-extraction
product.
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    NarrativeFinding,
    RawDocument,
)

_STOPWORDS = frozenset(
    """
    a an the and or but if then else for while with without within into onto from to of in on
    at by as is are was were be been being this that these those it its it's their our your my
    his her they them he she we you i not no yes will would could should can may might must
    shall than so such also more most less least very just about over under above below
    company companies quarter year years fiscal reported results revenue income
    """.split()
)

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'-]+")
_ENTITY_RE = re.compile(r"\b([A-Z][a-zA-Z0-9&]*(?:\s+[A-Z][a-zA-Z0-9&]*){0,3})\b")

MAX_KEYPHRASES = 10
MAX_ENTITIES = 10


def _keyphrases(text: str) -> list[str]:
    words = [w.lower() for w in _WORD_RE.findall(text) if w.lower() not in _STOPWORDS and len(w) > 2]
    unigram_counts = Counter(words)
    bigrams = [f"{a} {b}" for a, b in zip(words, words[1:])]
    bigram_counts = Counter(bigrams)

    candidates = Counter()
    candidates.update(unigram_counts)
    candidates.update({phrase: count * 2 for phrase, count in bigram_counts.items() if count > 1})

    return [phrase for phrase, _ in candidates.most_common(MAX_KEYPHRASES)]


def _entities(text: str) -> list[str]:
    matches = [m.strip() for m in _ENTITY_RE.findall(text)]
    counts = Counter(m for m in matches if len(m) > 2)
    return [entity for entity, _ in counts.most_common(MAX_ENTITIES)]


def extract_narrative_finding(document: RawDocument) -> NarrativeFinding:
    """Derive one `NarrativeFinding` from a fetched `RawDocument`."""

    return NarrativeFinding(
        ticker=document.ticker,
        source_type=document.source_type,
        source_id=document.source_id,
        published_at=document.published_at,
        keyphrases=_keyphrases(document.text),
        entities=_entities(document.text),
        fetched_at=datetime.now(timezone.utc),
    )


def extract_narrative_findings(documents: list[RawDocument]) -> list[NarrativeFinding]:
    return [extract_narrative_finding(document) for document in documents]
