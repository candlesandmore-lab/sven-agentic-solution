"""Label node: one bounded model call per cluster, producing a short topic label.

Per docs/implementation/01-narrative-cluster-discovery-surface.md's Interface Contracts:
input is a cluster's top keyphrases plus up to three representative excerpts; output is
exactly one short topic-label string, not a JSON payload.
"""

from __future__ import annotations

import os

import anthropic

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_LABEL_CHARS = 80
MAX_EXCERPTS = 3
MAX_EXCERPT_CHARS = 200

_SYSTEM_PROMPT = (
    "You label a cluster of stock tickers that share a narrative or topic, drawn from "
    "earnings reports, SEC filings, and news coverage. Given the cluster's top keyphrases "
    "and a few representative excerpts, respond with exactly one short topic label -- a "
    "few words naming the shared storyline, no punctuation-wrapped quotes, no JSON, no "
    "explanation. Never claim a specific price direction; the label names the narrative "
    "only, not a market call."
)


class LabelGenerationError(RuntimeError):
    """Raised when the label node's model call fails or returns an unusable label."""


def _build_user_prompt(top_keyphrases: list[str], excerpts: list[str]) -> str:
    excerpt_lines = "\n".join(f"- {excerpt[:MAX_EXCERPT_CHARS]}" for excerpt in excerpts[:MAX_EXCERPTS])
    return (
        f"Top keyphrases: {', '.join(top_keyphrases)}\n\n"
        f"Representative excerpts:\n{excerpt_lines or '(none available)'}\n\n"
        "Respond with the topic label only."
    )


def generate_topic_label(
    top_keyphrases: list[str],
    excerpts: list[str],
    *,
    client: anthropic.Anthropic | None = None,
    model: str = DEFAULT_MODEL,
    system_prompt: str = _SYSTEM_PROMPT,
    max_tokens: int = 32,
) -> str:
    """Call the configured model once to produce a short topic label for one cluster.

    `model`, `system_prompt`, and `max_tokens` default to this module's own constants but
    are normally overridden by `tts-coded-agent-config.yaml`'s `narrative-clusters-agent`
    section (see `NarrativeClustersAgent.__init__`), so a trader can change them without
    touching code.
    """

    resolved_client = client or anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = resolved_client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": _build_user_prompt(top_keyphrases, excerpts)}],
    )
    label = "".join(block.text for block in response.content if block.type == "text").strip()
    if not label:
        raise LabelGenerationError("Label node produced an empty label.")
    return label[:MAX_LABEL_CHARS]


def validate_label(label: str) -> bool:
    """Evaluate-node check for the label node's single-string output contract."""

    return bool(label) and 0 < len(label) <= MAX_LABEL_CHARS
