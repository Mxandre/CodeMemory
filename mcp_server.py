from __future__ import annotations

import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from db import init_db, insert_change, get_file_history, get_symbol_history

# STDIO MCP server do not use stdout to print logs, otherwise the MCP client will receive unexpected messages. So we configure logging to write to a file instead.
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("change-memory")


def _resolve_project_root(project_root: str) -> Path:
    p = Path(project_root).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Project root does not exist: {p}")
    return p


@mcp.tool()
def init_change_memory(project_root: str) -> dict:
    """
    Initialize the local change-memory database for a project.
    """
    root = _resolve_project_root(project_root)
    init_db(root)
    return {
        "status": "ok",
        "project_root": str(root),
        "db_path": str(root / ".debug_ai" / "change_memory.db"),
    }


@mcp.tool()
def store_change(
    project_root: str,
    file_path: str,
    symbol_type: str,
    symbol: str = "",
    change_reason: str = "",
    change_summary: str = "",
) -> dict:
    """
    Store one validated code change into the local change-memory DB.
    """
    root = _resolve_project_root(project_root)
    init_db(root)

    change_id = insert_change(
        project_root=root,
        symbol_type=symbol_type,
        symbol=symbol,
        change_reason=change_reason,
        change_summary=change_summary,
        file_path=file_path,
    )

    return {
        "status": "ok",
        "id": change_id,
        "file_path": file_path,
        "symbol_type": symbol_type,
        "symbol": symbol,
    }


@mcp.tool()
def get_file_history_tool(
    project_root: str,
    file_path: str,
    limit: int = 5,
) -> dict:
    """
    Return recent validated changes for one file.
    """
    root = _resolve_project_root(project_root)
    init_db(root)

    items = get_file_history(
        project_root=root,
        file_path=file_path,
        limit=limit,
    )
    return {
        "status": "ok",
        "count": len(items),
        "items": items,
    }


@mcp.tool()
def get_symbol_history_tool(
    project_root: str,
    file_path: str,
    symbol: str,
    limit: int = 5,
) -> dict:
    """
    Return recent validated changes for one symbol in one file.
    """
    root = _resolve_project_root(project_root)
    init_db(root)

    items = get_symbol_history(
        project_root=root,
        file_path=file_path,
        symbol=symbol,
        limit=limit,
    )
    return {
        "status": "ok",
        "count": len(items),
        "items": items,
    }


if __name__ == "__main__":
    mcp.run()