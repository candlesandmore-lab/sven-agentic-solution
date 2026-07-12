"""Runtime configuration for the Technical Trader Solution's own coded agents.

This is a separate file and loader from `agent-building-agent`'s own
`coded-agent-config.yaml`: that file configures the four framework coded agents used by
the *development flow itself* (story-telling-agent, review-validation-agent, etc.) and its
loader (`agent_building_agent.coded_agents.config`) validates `coded_agents` section keys
against a closed set of those four slugs -- it cannot and should not be extended with a
deliverable's own coded agents. `tts-coded-agent-config.yaml` follows the same shape (one
YAML file, a section per coded sub-agent, LLM endpoint + model + user-reviewable system
prompt) for the same reason that pattern exists: so a human trader can review and edit the
model and prompt driving their solution's coded agents without touching code.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

DEFAULT_CONFIG_PATH = Path("tts-coded-agent-config.yaml")


class LlmEndpointConfig(BaseModel):
    provider: str
    base_url: str
    api_key_env: str


class CodedAgentSectionConfig(BaseModel):
    llm_endpoint: LlmEndpointConfig
    model: str
    system_prompt: str
    max_tokens: int = 8192


class CodedAgentRuntimeConfig(BaseModel):
    schema_version: int
    coded_agents: dict[str, CodedAgentSectionConfig]


def load_runtime_config(path: Path | str = DEFAULT_CONFIG_PATH) -> CodedAgentRuntimeConfig | None:
    """Load `tts-coded-agent-config.yaml`, or `None` when it has not been created yet.

    Absence is not an error: every coded agent in this workspace falls back to its own
    hardcoded default model and system prompt when no config file overrides them, so a
    trader can start using the solution before ever touching this file.
    """

    resolved = Path(path)
    if not resolved.is_file():
        return None
    with resolved.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return CodedAgentRuntimeConfig.model_validate(raw)


def get_agent_section(
    config: CodedAgentRuntimeConfig | None, agent_slug: str
) -> CodedAgentSectionConfig | None:
    if config is None:
        return None
    return config.coded_agents.get(agent_slug)
