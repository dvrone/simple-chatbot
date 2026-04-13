import os

import pytest

from src.core.memory import Memory


@pytest.fixture
def memory(tmp_path):
    """Create a temporary memory instance for testing."""
    db_path = str(tmp_path / "test_memory.db")
    return Memory(db_path=db_path)


class TestMemory:
    """Tests for the Memory class."""

    def test_remember_and_recall(self, memory):
        """Should store and retrieve a value."""
        memory.remember("name", "Diyorbek")
        assert memory.recall("name") == "Diyorbek"

    def test_recall_nonexistent_key(self, memory):
        """Should return None for a key that doesn't exist."""
        assert memory.recall("nonexistent") is None

    def test_remember_overwrites(self, memory):
        """Should overwrite existing value."""
        memory.remember("name", "Diyorbek")
        memory.remember("name", "Alex")
        assert memory.recall("name") == "Alex"

    def test_remember_mood(self, memory):
        """Should store mood in mood_history table."""
        memory.remember_mood("happy")
        assert memory.recall_last_mood() == "happy"

    def test_recall_last_mood(self, memory):
        """Should return the most recently stored mood."""
        memory.remember_mood("happy")
        memory.remember_mood("sad")
        assert memory.recall_last_mood() == "sad"

    def test_recall_last_mood_empty(self, memory):
        """Should return None when no mood is stored."""
        assert memory.recall_last_mood() is None

    def test_add_history(self, memory):
        """Should add messages to history."""
        memory.add("user", "hello")
        memory.add("bot", "hi")
        assert len(memory.history) == 2

    def test_history_max_limit(self, memory):
        """Should not exceed max_history limit."""
        for i in range(15):
            memory.add("user", f"message {i}")
        assert len(memory.history) == memory.max_history

    def test_get_context(self, memory):
        """Should return formatted conversation context."""
        memory.add("user", "hello")
        memory.add("bot", "hi there")
        context = memory.get_context()
        assert "User: hello" in context
        assert "Maki: hi there" in context

    def test_clear(self, memory):
        """Should clear both history and database."""
        memory.remember("name", "Diyorbek")
        memory.add("user", "hello")
        memory.clear()
        assert memory.recall("name") is None
        assert len(memory.history) == 0
