import sqlite3
from pathlib import Path


class Memory:
    """Handles persistent and in-session memory for the chatbot."""

    def __init__(self, db_path: str = "data/memory.db", max_history: int = 10):
        self.db_path = db_path
        self.max_history = max_history
        self.history = []
        Path(db_path).parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database and create tables if not exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS user_data (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS mood_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mood TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def remember(self, key: str, value: str):
        """Store a key-value pair persistently in the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO user_data (key, value) VALUES (?, ?)",
                (key, value),
            )
            conn.commit()

    def recall(self, key: str) -> str | None:
        """Retrieve a stored value by key from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM user_data WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def remember_mood(self, mood: str):
        """Store the user's current mood in the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO mood_history (mood) VALUES (?)",
                (mood,),
            )
            conn.commit()

    def recall_last_mood(self) -> str | None:
        """Retrieve the most recently stored mood."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT mood FROM mood_history ORDER BY timestamp DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return row[0] if row else None

    def add(self, role: str, text: str):
        """Add a message to the in-session conversation history."""
        self.history.append({"role": role, "text": text})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self) -> str:
        """Return the conversation history as a formatted string."""
        if not self.history:
            return ""
        context = []
        for msg in self.history:
            prefix = "User" if msg["role"] == "user" else "Maki"
            context.append(f"{prefix}: {msg['text']}")
        return "\n".join(context)

    def clear(self):
        """Clear both in-session history and persistent database."""
        self.history = []
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM user_data")
            conn.commit()
