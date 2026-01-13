"""
Entry point used by MCP CLI (`mcp run .../main.py`) per `config.txt`.

This simply runs the same FastMCP server defined in `app.py`.
"""

from app import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")

