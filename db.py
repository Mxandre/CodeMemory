import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

def get_db_path(project_root : Path) -> Path :
    return project_root / ".debug_ai" / "change_memory.db"

def ensure_db_dir(project_root : Path):
    db_dir = project_root/ ".debug_ai" 
    db_dir.mkdir(parents=True, exist_ok=True)



def init_db(project_root : Path) :
    ensure_db_dir(project_root)
    db_path = get_db_path(project_root)
    conn = sqlite3.connect(db_path)
    with open("schema.sql", "r") as f :
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# --------Insert--------------
def insert_change(
    project_root : Path,
    symbol_type : str, 
    symbol : Optional[str],
    change_reason: str,
    change_summary: str,
    file_path: str
) -> int:
    db_path = get_db_path(project_root)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    timestamp = datetime.now(timezone.utc)

    c.execute(
        """
        INSERT INTO  changes (
        timestamp, symbol_type, symbol,
            change_reason, change_summary, file_path
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (timestamp, symbol_type, symbol, change_reason, change_summary, file_path),
        )
    
    change_id = c.lastrowid

    conn.commit()
    conn.close()

    return change_id


# --------------Query : file -----------------
def get_file_history(
    project_root : Path,
    file_path: str,
    limit: int = 5
) -> List[Dict] : 
    db_path = get_db_path(project_root)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(
       """
        SELECT id, timestamp, symbol_type, symbol,
               change_reason, change_summary, file_path
        FROM changes
        WHERE file_path = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (file_path, limit), 
    )

    rows = c.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]

def _row_to_dict(row) -> Dict:
    return{
        "id": row[0],
        "timestamp": row[1],
        "symbol_type": row[2],
        "symbol": row[3],
        "change_reason": row[4],
        "change_summary": row[5],
        "file_path": row[6],
    }

def get_symbol_history(
    project_root: Path,
    file_path: str,
    symbol: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    db_path = get_db_path(project_root)
    conn = sqlite3.connect(db_path)
    try:
        c = conn.cursor()
        c.execute(
            """
            SELECT
                id,
                timestamp,
                symbol_type,
                symbol,
                change_reason,
                change_summary,
                file_path
            FROM changes
            WHERE file_path = ? AND symbol = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (file_path, symbol, limit),
        )
        rows = c.fetchall()
        return [_row_to_dict(row) for row in rows]
    finally:
        conn.close()