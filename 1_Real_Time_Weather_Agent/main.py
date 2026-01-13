import sys
from mcp.server.fastmcp import FastMCP 
from tools.weather import get_weather 
from typing import Any

# Ensure UTF-8 output so tool responses can include non-ASCII characters (e.g., wttr.in emojis)
# without crashing on Windows consoles / pipes using legacy encodings.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

mcp = FastMCP("Weather Checker")

@mcp.tool()
async def check_weather(location: str) -> str:
    """
    Get weather information for a specified location.
    """
    return get_weather(location)


if __name__ == "__main__":
    mcp.run(transport="stdio")