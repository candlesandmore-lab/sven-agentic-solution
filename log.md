/Users/frank/SynologyDrive/Drive/LaptopOnly/Programming/agentic-trading-solutions/sven-agentic-solution
Follow steps in INSTALL.md
OS-X: set up ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

# Remove install artifacts to avoid confusion on files (like skills/agent)
rm -rf agent-dev-agent

# VS-Code refresh
<reload window if in VS-Code>

# Test
"what is the status of my git repo" -> should use the MCP tool 'git_repository_context'