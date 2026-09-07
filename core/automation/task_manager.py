import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path("data/memory/jarvis_tasks.db")


class TaskManager:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(DB_PATH) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            db.commit()

    def create_task(self, name):
        now = datetime.now().isoformat()

        with sqlite3.connect(DB_PATH) as db:
            cursor = db.execute(
                """
                INSERT INTO tasks
                (name, status, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, "pending", now, now)
            )
            db.commit()

            return cursor.lastrowid

    def update_status(self, task_id, status):
        now = datetime.now().isoformat()

        with sqlite3.connect(DB_PATH) as db:
            db.execute(
                """
                UPDATE tasks
                SET status = ?, updated_at = ?
                WHERE id = ?
                """,
                (status, now, task_id)
            )
            db.commit()

    def get_task(self, task_id):
        with sqlite3.connect(DB_PATH) as db:
            row = db.execute(
                """
                SELECT id, name, status, created_at, updated_at
                FROM tasks
                WHERE id = ?
                """,
                (task_id,)
            ).fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "created_at": row[3],
            "updated_at": row[4]
        }
