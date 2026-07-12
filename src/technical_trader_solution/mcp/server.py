"""Root FastMCP server for the Technical Trader Solution.

Per-capability tool modules (for example ``narrative_clusters``) register their tools on
``mcp`` via decorator import side effects; import them below so ``main()`` (and the
``tts-mcp-serve`` entry point) always exposes every registered capability.
"""

from __future__ import annotations

from fastmcp import FastMCP

mcp = FastMCP("technical-trader-solution")

__all__ = ["mcp"]

# Imported for their @mcp.tool() registration side effects.
from technical_trader_solution.mcp import narrative_clusters as _narrative_clusters  # noqa: E402,F401


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
