import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/memory/jarvis_memory.db")


def save_memory(key, value):
    now = datetime.now().isoformat()

    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "DELETE FROM memories WHERE key = ?",
            (key,)
        )
        db.execute(
            """
            INSERT INTO memories (key, value, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (key, value, now, now)
        )
        db.commit()


def get_memories(key):
    with sqlite3.connect(DB_PATH) as db:
        rows = db.execute(
            "SELECT value FROM memories WHERE key = ? ORDER BY updated_at DESC",
            (key,)
        ).fetchall()

    return [row[0] for row in rows]


def delete_memory(key):
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "DELETE FROM memories WHERE key = ?",
            (key,)
        )
        db.commit()


def search_memories(query, limit=5):
    query = query.strip()

    if not query:
        return []

    pattern = f"%{query}%"

    with sqlite3.connect(DB_PATH) as db:
        rows = db.execute(
            """
            SELECT key, value
            FROM memories
            WHERE key LIKE ? OR value LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (pattern, pattern, limit)
        ).fetchall()

    return [{"key": key, "value": value} for key, value in rows]
