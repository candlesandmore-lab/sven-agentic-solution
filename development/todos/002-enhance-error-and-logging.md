# Goal:
Enhance the generated technical_trader_solution with proper error handling and logging for debug.

# Success criteria:
- The technical trader solution flow and core implementation stays as is.
- The control and data flow operation are properly logged in a log file.
- Error handling is implemented in core and user surfaces, with proper error messages on CLI and MCP interface and proper exception throwing in SDK API.

# Implementation hints:
- The agent-dev-agent has been enhanced (agent/skill + coded agents) with required instructions on how to do logging and error handling.


>>> summary:

Story 002 is complete. Working tree is clean except the three pre-existing, unrelated log-file deletions from agent-building-agent's own MCP server restart (now writing to agent_building_agent/ per its documented convention) — I left those alone since they're outside this story's scope.

Summary of what shipped:

Story: development/backlog/implemented/002-enhance-error-and-logging.yaml — full flow from todo through implementation, all review gates passed clean.
Architecture (docs/architecture/01-technical-trader-solution.md v0.5): new Logging and Error Handling cross-cutting section, plus the instructed_agent_only classification.
Implementation spec (docs/implementation/02-logging-and-error-handling.md v0.3): the full logging/error contract.
Code: errors.py (new domain exception hierarchy), extended logging.py (masked, run-coordinated shared log file, root/third-party logger redirection), and wiring across CLI, SDK, MCP, and the dashboard.
Tests: 46 passed, 1 skipped (no FMP_API_KEY), including new unit and interface tests, plus a real end-to-end CLI smoke test.
One thing worth flagging: while drafting the story, the coded agent's tool calls initially failed twice because I guessed wrong input field names — I found and fixed the actual contract by reading each coded agent's source directly, which is now a reliable pattern if this comes up again.
