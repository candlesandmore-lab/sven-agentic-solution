"""Narrative Extraction and Clustering Pipeline (story 001, US-015).

Coded agent per docs/implementation/01-narrative-cluster-discovery-surface.md's
Coded-Agent Flow: entry, fetch, extract, cluster, label, trend, persist, evaluate, and
terminal nodes on the workspace's uniform ClaudeCode SDK base
(technical_trader_solution.coded_agents.base).
"""

from technical_trader_solution.coded_agents.narrative_clusters_agent.agent import (
    NarrativeClustersAgent,
)

__all__ = ["NarrativeClustersAgent"]
