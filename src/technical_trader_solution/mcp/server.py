"""Root FastMCP server for the Technical Trader Solution.

Per-capability tools (for example the ``narrative_clusters`` tools) are registered on
``mcp`` by the task that wires that capability's invocation surfaces. This module is a
scaffold placeholder: it defines the server instance only.
"""

from __future__ import annotations

from fastmcp import FastMCP

mcp = FastMCP("technical-trader-solution")

__all__ = ["mcp"]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
