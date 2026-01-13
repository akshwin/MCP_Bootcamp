import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("terminal")

# Default workspace (works both on host + in the provided Docker command that mounts to /root/mcp/workspace)
DEFAULT_WORKSPACE = os.getenv("MCP_WORKSPACE", os.path.expanduser("~/mcp/workspace"))

def _workspace_root() -> Path:
    return Path(DEFAULT_WORKSPACE).expanduser().resolve()


def _safe_path(relative_path: str) -> Path:
    """
    Resolve a user-provided path safely under DEFAULT_WORKSPACE.
    Prevents path traversal like ../../secrets.txt.
    """
    root = _workspace_root()
    target = (root / relative_path).expanduser().resolve()
    if root not in target.parents and target != root:
        raise ValueError(f"Path must be under workspace: {root}")
    return target


@mcp.tool()
async def run_command(command: str) -> str:
    """
    Run a shell command and return stdout (or stderr if stdout is empty).
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=DEFAULT_WORKSPACE if os.path.isdir(DEFAULT_WORKSPACE) else None,
            capture_output=True,
            text=True,
        )
        return (result.stdout or result.stderr or "").strip()
    except Exception as e:
        return str(e)


@mcp.tool()
async def create_file(filename: str, content: str = "", overwrite: bool = False) -> str:
    """
    Create a file under the workspace. (Matches common agent expectations like `create_file`.)
    """
    try:
        path = _safe_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not overwrite:
            return f"File already exists: {filename} (set overwrite=true to replace)"
        path.write_text(content, encoding="utf-8")
        return f"Created: {filename}"
    except Exception as e:
        return str(e)


@mcp.tool()
async def write_file(filename: str, content: str, append: bool = False) -> str:
    """
    Write text content to a file under the workspace.
    """
    try:
        path = _safe_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        with path.open(mode, encoding="utf-8") as f:
            f.write(content)
        return f"Wrote: {filename}"
    except Exception as e:
        return str(e)


@mcp.tool()
async def read_file(filename: str, max_chars: int = 20000) -> str:
    """
    Read a text file under the workspace (truncated to max_chars).
    """
    try:
        path = _safe_path(filename)
        if not path.exists():
            return f"Not found: {filename}"
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > max_chars:
            return text[:max_chars] + "\n... (truncated) ..."
        return text
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    mcp.run(transport="stdio")

