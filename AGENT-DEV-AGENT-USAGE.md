<!-- Copyright (c) 2026 agent-building-agent contributors -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Source: https://TBD (training course) -->

# Agent-Dev-Agent Usage Guide

This document explains how to set up and trigger the instructed agents, skills, and coded agents installed by `agent-building-agent` in each supported framework target. It is installed at your workspace root alongside `coded-agent-config.yaml` and `INSTALL.md`.

For wheel installation and release-package steps, see `INSTALL.md`. This guide focuses on how to use the installed agents and tools.

## Quick start

After installing the wheel and running `agent-building-agent install` (see `INSTALL.md`), two things are ready:

1. **Prompted assets** — agent markdown, skills, and sub-skills are rendered into the framework-specific locations listed below.
2. **MCP server** — the agent-building-agent MCP server is registered so agents can call git, Python, pytest, YAML-validation, and coded-agent tools.

To start working:

1. Open your workspace in your chosen framework (VS Code with Copilot, Claude CLI, Cline, etc.).
2. Select `agent-dev-agent` from the framework's agent surface (or start a chat in Cline).
3. Describe your development task — the agent-dev-agent will follow the development flow.

For Cline targets, one extra manual step is required because Cline reads MCP config from a global settings file, not from workspace files — see [Cline MCP setup](#cline-mcp-setup-global-config) below.

## Supported framework targets

| Target | Agents | Skills | MCP config |
|---|---|---|---|
| `vs-code-ghcp` | `.github/agents/*.agent.md` | `.github/skills` | `.vscode/mcp.json` |
| `vs-code-claude` | `.vscode/claude/agents/*.md` | `.vscode/claude/skills` | `.vscode/mcp.json` |
| `cli-claude` | `.claude/agents/*.md` | `.claude/skills` | `.mcp.json` |
| `cli-cline` | `.clinerules/agents/*.md` | `.clinerules/skills` | global Cline settings file (see below) |
| `vs-code-cline` | `.clinerules/agents/*.md` | `.clinerules/skills` | global Cline settings file (see below) |

The installer writes the MCP server entry with an **absolute path** to the `agent-building-agent` executable (resolved from `PATH` or `<workspace>/.venv/bin/`) and an absolute `cwd` pointing to your workspace root. This ensures the framework host can launch the server regardless of its own `PATH` or working directory.

### Cline MCP setup (global config)

**Cline does not read workspace `.mcp.json` or `.vscode/mcp.json`.** Cline reads MCP server configuration from a single **global** settings file inside VS Code's `globalStorage` directory:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| Windows | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json` |
| Linux | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |

If you use a VS Code distribution other than standard VS Code, replace the `Code` segment accordingly: `Code - Insiders`, `Cursor`, `VSCodium`, or `Windsurf`.

To register the agent-building-agent MCP server in Cline:

1. Open the global `cline_mcp_settings.json` file in your editor.
2. Add the `agent-building-agent` entry under `mcpServers` with the absolute path to your workspace's `agent-building-agent` executable and the absolute `cwd`:

```json
{
  "mcpServers": {
    "agent-building-agent": {
      "command": "/absolute/path/to/your/workspace/.venv/bin/agent-building-agent",
      "args": ["mcp-serve"],
      "cwd": "/absolute/path/to/your/workspace"
    }
  }
}
```

3. Reload VS Code (Cmd+Shift+P → "Developer: Reload Window") or restart the Cline extension. Cline only reads this config at startup.
4. Open the Cline sidebar — the `agent-building-agent` server should appear in the MCP section.
5. If it shows a connection error, click the refresh/retry icon next to the server.

Because the config is global, the server entry is available in **every** VS Code workspace you open with Cline. The `cwd` you set determines which workspace the server runs from. If you want to use agent-building-agent in a different workspace later, update the `cwd` and `command` paths in the global settings file.

The workspace `.mcp.json` and `.vscode/mcp.json` files the installer writes are still valid for Claude Code CLI, Cursor, and VS Code native MCP — they just are not read by Cline. Both files can coexist without conflict.

## Instructed agents and skills

The top-level agent is `agent-dev-agent`, an instructed orchestrator. It routes work to specialist agents and skills:

- `agent-dev-agent` — top-level orchestrator (instructed, always).
- `architect-planning-agent` — architecture and implementation planning (instructed).
- `python-creation-agent` — Python package and interface creation (instructed).
- `story-telling-agent` — coded-agent front door for todo-to-story generation.
- `review-validation-agent` — coded-agent front door for review gate and refinement handling.
- `instructed-agent-creation-agent` — coded-agent front door for agent, skill, and sub-skill creation.
- `qa-agent` — coded-agent front door for executable and prompt validation.
- `coded-subagent-creation-agent` — instructed agent for Claude-SDK/LangGraph coded-agent implementation.

### How to invoke the top-level agent in each framework

- **vs-code-ghcp**: Select `agent-dev-agent` from the GitHub Copilot Chat agent picker in VS Code. The agent definition is at `.github/agents/agent-dev-agent.agent.md`.
- **vs-code-claude**: Select `agent-dev-agent` from the Claude agent surface in VS Code. The agent definition is at `.vscode/claude/agents/agent-dev-agent.md`.
- **cli-claude**: Select `agent-dev-agent` from the Claude CLI agent list. The agent definition is at `.claude/agents/agent-dev-agent.md`.
- **cli-cline**: Cline does not have a per-agent routing surface. The agent and skill markdown under `.clinerules/` is loaded as workspace rules. Start a chat with Cline and describe your development task; the rules guide Cline to follow the agent-dev-agent development flow.
- **vs-code-cline**: Same as `cli-cline` — Cline loads all markdown under `.clinerules/` as workspace rules. Start a chat and describe your task.

### Skills and sub-skills

Skills are loaded by the top-level agent and specialist agents through their `agent.md` references. Each skill has a `SKILL.md` entry point and may have sub-skills under `sub-skills/`. The framework target determines where these files are rendered (see the table above), but the agent references them by relative path so the same skill content works across all targets.

## Coded sub-agents

The four coded sub-agents are Python/LangGraph implementations invoked over MCP, CLI, or SDK — not markdown files. They are configured by `coded-agent-config.yaml` at the workspace root.

### Coded agent slugs

- `story-telling-agent` — transforms todo input into backlog-ready story YAML.
- `review-validation-agent` — executes review steps, produces findings, and emits gate decisions.
- `instructed-agent-creation-agent` — generates agent markdown, skill, and sub-skill assets.
- `qa-agent` — runs unit, interface, prompt, and demo validation layers.

### Invocation surfaces

**MCP tool** (available to all framework targets via the registered MCP config):

The `coded_agent_invoke` MCP tool accepts:
- `agent_slug` — one of the four slugs above.
- `task_id` — a caller-supplied id; a new id starts a run, an existing id resumes persisted state.
- `inputs` — agent-specific input payload (dict).
- `answers` — answers to a prior failure contract's questions (dict), used to resume.

**CLI**:

```sh
agent-building-agent coded-agents <slug> --task-id <id> --input '<json>'
# or with a file:
agent-building-agent coded-agents <slug> --task-id <id> --input-file <path.json>
```

The four CLI subcommands are `story-telling`, `review-validation`, `instructed-agent-creation`, and `qa`.

**SDK**:

```python
from agent_building_agent.sdk import AgentBuildingAgentSdk

sdk = AgentBuildingAgentSdk()
response = sdk.run_coded_agent(
    agent_slug="qa-agent",
    task_id="smoke-test",
    inputs={"validation_scope": ["pytest"], "pytest_scope": "tests/test_models.py"},
)
```

### Failure and resume

If a coded agent cannot complete its task after five internal iterations, it returns `status: failed_after_iterations` with `questions` for you to answer. Re-run the same command with the same `task_id` and an `--answers` payload (CLI) or `answers` dict (MCP/SDK) to resume.

## MCP tools

The `agent-building-agent mcp-serve` MCP server registers the following tools, available to every framework target:

**Git tools**:
- `git_repository_context` — inspect repository state, status, branch list, log, and show.
- `git_change_review` — review working-tree or staged diffs.
- `git_staging` — stage approved file paths.
- `git_commit_workflow` — create an approved commit.
- `git_branch_sync` — manage branches and remote synchronization (branch_create, switch, pull, push).

**Execution tools**:
- `render_python_execution` — render a Python command for a module or script.
- `render_pytest_execution` — render the pytest command for a test scope.
- `validate_yaml` — validate YAML files and return structured parse findings.

**Coded-agent tool**:
- `coded_agent_invoke` — invoke any of the four coded sub-agents.

## `coded-agent-config.yaml`

Located at the workspace root. Each coded sub-agent section carries:
- `llm_endpoint` — provider (`claude` or `openai-compatible`), `base_url`, and `api_key_env`.
- `model` — model name.
- `system_prompt` — user-reviewable system prompt.
- `max_tokens` — maximum output tokens for structured payloads (default 8192).

Edit this file to change a coded agent's provider, model, or system prompt. Re-running `install --mode update` preserves your `system_prompt`, `model`, and `llm_endpoint` fields and only merges in new non-user-owned fields.