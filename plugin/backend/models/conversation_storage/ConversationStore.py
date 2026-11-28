import json
import sqlite3
from typing import Any

class ConversationStore:
    def __init__(self, db_path: str = "sessions.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, session_id TEXT, payload TEXT)"
        )

    def append(self, session_id: str, message: dict[str, Any]) -> None:
        self.conn.execute(
            "INSERT INTO messages (session_id, payload) VALUES (?, ?)",
            (session_id, json.dumps(message)),
        )
        self.conn.commit()

    def get_window(self, session_id: str, limit: int) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT payload FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
        messages = [json.loads(r[0]) for r in reversed(rows)]
        while messages and messages[0].get("role") == "tool":
            messages.pop(0)
        return messages