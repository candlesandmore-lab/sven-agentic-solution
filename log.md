/Users/frank/SynologyDrive/Drive/LaptopOnly/Programming/agentic-trading-solutions/sven-agentic-solution
Follow steps in INSTALL.md
OS-X: set up ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

{
  "mcpServers": {
    "agent-building-agent": {
      "command": "bash",
      "args": [
        "-c",
        "source /Users/frank/SynologyDrive/Drive/LaptopOnly/Programming/agentic-trading-solutions/.env && exec uv run python -m agent_building_agent",
        "mcp-serve"
      ],
      "cwd": "/Users/frank/SynologyDrive/Drive/LaptopOnly/Programming/agentic-trading-solutions/sven-agentic-solution"
    }
  }
}

Ensure that environment variables include API keys for LLMs

# Remove install artifacts to avoid confusion on files (like skills/agent)
rm -rf agent-dev-agent

# VS-Code refresh
<reload window if in VS-Code>

# Test
"what is the status of my git repo" -> should use the MCP tool 'git_repository_context'

<-- first commit -->

# Setup user data
mkdir -p user-input/docu
cp -pr /Users/frank/SynologyDrive/Drive/LaptopOnly/Programming/agentic-trading-solutions/Agent-Build-Agents/docu/digest-aids user-input/docu
cp -pr /Users/frank/SynologyDrive/Drive/LaptopOnly/Programming/agentic-trading-solutions/Agent-Build-Agents/docu/inputs user-input/docu

<-- second commit -->

# Let it work ...

Created "development/todos/001-start-us-011.md"

Prompt: "I have a todo development/todos/001-start-us-011.md, use the agent-dev-agent to create a story for it and implement it" 