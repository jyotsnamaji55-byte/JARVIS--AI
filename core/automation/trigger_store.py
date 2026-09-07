import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("data/automation/triggers.db")


class TriggerStore:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _init_db(self):
        with self._connect() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS triggers (
                    name TEXT PRIMARY KEY,
                    event_name TEXT NOT NULL,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            db.commit()

    def save(self, name, event_name, enabled=True):
        now = datetime.now().isoformat()

        with self._connect() as db:
            db.execute("""
                INSERT INTO triggers
                    (name, event_name, enabled, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    event_name = excluded.event_name,
                    enabled = excluded.enabled,
                    updated_at = excluded.updated_at
            """, (
                name,
                event_name,
                int(enabled),
                now,
                now
            ))
            db.commit()

    def get(self, name):
        with self._connect() as db:
            row = db.execute("""
                SELECT name, event_name, enabled
                FROM triggers
                WHERE name = ?
            """, (name,)).fetchone()

        if not row:
            return None

        return {
            "name": row[0],
            "event_name": row[1],
            "enabled": bool(row[2])
        }

    def list_all(self):
        with self._connect() as db:
            rows = db.execute("""
                SELECT name, event_name, enabled
                FROM triggers
                ORDER BY name
            """).fetchall()

        return [
            {
                "name": row[0],
                "event_name": row[1],
                "enabled": bool(row[2])
            }
            for row in rows
        ]

    def set_enabled(self, name, enabled):
        with self._connect() as db:
            db.execute("""
                UPDATE triggers
                SET enabled = ?, updated_at = ?
                WHERE name = ?
            """, (
                int(enabled),
                datetime.now().isoformat(),
                name
            ))
            db.commit()

    def delete(self, name):
        with self._connect() as db:
            db.execute(
                "DELETE FROM triggers WHERE name = ?",
                (name,)
            )
            db.commit()
