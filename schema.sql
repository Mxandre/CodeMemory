CREATE TABLE IF NOT EXISTS changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT NOT NULL,
    symbol_type   TEXT NOT NULL,
    symbol  TEXT,
    change_reason TEXT NOT NULL,
    change_summary TEXT NOT NULL, 
    file_path  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_changes_file_path ON changes(file_path);
CREATE INDEX IF NOT EXISTS idx_changes_symbol ON changes(symbol);
CREATE INDEX IF NOT EXISTS idx_changes_timestamp ON changes(timestamp);