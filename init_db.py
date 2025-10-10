from shared import DB_PATH
import sqlite3


DDL = """
CREATE TABLE IF NOT EXISTS telemetry (
id INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp REAL NOT NULL,
type TEXT,
device_id TEXT,
data TEXT NOT NULL
);


CREATE INDEX IF NOT EXISTS idx_type_timestamp ON telemetry(type, timestamp);
"""


if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(DDL)
    conn.commit()
    conn.close()
    print("initialized:", DB_PATH)