import sqlite3
from pathlib import Path


class Memory:
    def __init__(self, db_path: str = "data/memory.db", max_history: int = 10):
        self.db_path = db_path
        self.max_history = max_history
        self.history = []
        Path(db_path).parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_data (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """
            )
            conn.commit()

    def remember(self, key: str, value: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO user_data (key, value) VALUES (?, ?)",
                (key, value),
            )
            conn.commit()

    def recall(self, key: str) -> str | None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM user_data WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def add(self, role: str, text: str):
        self.history.append({"role": role, "text": text})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self) -> str:
        if not self.history:
            return ""
        context = []
        for msg in self.history:
            prefix = "Foydalanuvchi" if msg["role"] == "user" else "Bot"
            context.append(f"{prefix}: {msg['text']}")
        return "\n".join(context)

    def clear(self):
        self.history = []
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM user_data")
            conn.commit()
