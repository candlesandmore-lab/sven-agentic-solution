"""Root FastMCP server for the Technical Trader Solution.

Per-capability tool modules (for example ``narrative_clusters``) register their tools on
``mcp`` via decorator import side effects; import them below so ``main()`` (and the
``tts-mcp-serve`` entry point) always exposes every registered capability.
"""

from __future__ import annotations

from fastmcp import FastMCP

from technical_trader_solution.logging import configure_logger

# Configure logging before constructing FastMCP: FastMCP configures the root logger with
# its own handler purely by being constructed (regardless of which command runs), so
# configure_logger must run first to guarantee the root logger already carries the masked,
# shared-log-file handlers before any component's log records start propagating to it.
configure_logger("technical_trader_solution")

mcp = FastMCP("technical-trader-solution")

__all__ = ["mcp"]

# Imported for their @mcp.tool() registration side effects.
from technical_trader_solution.mcp import narrative_clusters as _narrative_clusters  # noqa: E402,F401


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
