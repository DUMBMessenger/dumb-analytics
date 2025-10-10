import sqlite3
from shared import DB_PATH
from contextlib import contextmanager

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    try:
        yield conn
    finally:
        conn.close()