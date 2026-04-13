import pytest

from src.core.memory import Memory
from src.features.handlers import MemoryHandler, PersonalityHandler


@pytest.fixture
def memory(tmp_path):
    """Create a temporary memory instance for testing."""
    db_path = str(tmp_path / "test_memory.db")
    return Memory(db_path=db_path)


@pytest.fixture
def memory_handler(memory):
    """Create a MemoryHandler instance for testing."""
    return MemoryHandler(memory)


@pytest.fixture
def personality_handler(memory):
    """Create a PersonalityHandler instance for testing."""
    return PersonalityHandler(memory)


class TestMemoryHandler:
    """Tests for the MemoryHandler class."""

    def test_extract_name(self, memory_handler, memory):
        """Should extract and store name from text."""
        memory_handler.extract("my name is Diyorbek")
        assert memory.recall("name") == "Diyorbek"

    def test_extract_name_call_me(self, memory_handler, memory):
        """Should extract name using 'call me' trigger."""
        memory_handler.extract("call me Alex")
        assert memory.recall("name") == "Alex"

    def test_extract_age(self, memory_handler, memory):
        """Should extract and store age from text."""
        memory_handler.extract("i am 25 years old")
        assert memory.recall("age") == "25"

    def test_extract_city_english(self, memory_handler, memory):
        """Should extract and store city from English text."""
        memory_handler.extract("i live in Tashkent")
        assert memory.recall("city") == "Tashkent"

    def test_recall_name(self, memory_handler, memory):
        """Should return stored name."""
        memory.remember("name", "Diyorbek")
        assert memory_handler.recall_name() == "Your name is Diyorbek!"

    def test_recall_name_empty(self, memory_handler):
        """Should return default message when name not stored."""
        assert (
            memory_handler.recall_name()
            == "I don't know your name yet, please tell me!"
        )

    def test_recall_age(self, memory_handler, memory):
        """Should return stored age."""
        memory.remember("age", "25")
        assert memory_handler.recall_age() == "You are 25 years old!"

    def test_recall_city(self, memory_handler, memory):
        """Should return stored city."""
        memory.remember("city", "Tashkent")
        assert memory_handler.recall_city() == "You live in Tashkent!"

    def test_detect_mood_happy(self, memory_handler):
        """Should detect happy mood."""
        assert memory_handler.detect_mood("i feel happy today") == "happy"

    def test_detect_mood_tired(self, memory_handler):
        """Should detect tired mood."""
        assert memory_handler.detect_mood("i am so tired") == "tired"

    def test_detect_mood_none(self, memory_handler):
        """Should return None when no mood detected."""
        assert memory_handler.detect_mood("what time is it") is None

    def test_handle_mood_negation(self, memory_handler):
        """Should return None for negated mood."""
        result = memory_handler.handle_mood("i am not tired")
        assert result is None

    def test_handle_mood_stores(self, memory_handler, memory):
        """Should store detected mood."""
        memory_handler.handle_mood("i am so happy")
        assert memory.recall_last_mood() == "happy"


class TestPersonalityHandler:
    """Tests for the PersonalityHandler class."""

    def test_greet_without_name(self, personality_handler):
        """Should return greeting without name."""
        response = personality_handler.greet()
        assert any(w in response for w in ["Hi", "Hello", "Hey"])
        assert "🌸" in response or "💜" in response

    def test_greet_with_name(self, personality_handler, memory):
        """Should return personalized greeting with name."""
        memory.remember("name", "Diyorbek")
        response = personality_handler.greet()
        assert "Diyorbek" in response

    def test_farewell_without_name(self, personality_handler):
        """Should return farewell without name."""
        response = personality_handler.farewell()
        assert any(w in response for w in ["Goodbye", "See you", "Bye"])

    def test_farewell_with_name(self, personality_handler, memory):
        """Should return personalized farewell with name."""
        memory.remember("name", "Diyorbek")
        response = personality_handler.farewell()
        assert "Diyorbek" in response

    def test_unknown_response(self, personality_handler):
        """Should return unknown response."""
        response = personality_handler.unknown()
        assert any(w in response for w in ["didn't", "Sorry", "Hmm"])

    def test_add_follow_up(self, personality_handler):
        """Should occasionally add follow-up phrase."""
        # Run 20 times to ensure follow-up appears at least once
        results = [personality_handler.add_follow_up("Hello!") for _ in range(20)]
        assert any("\n\n_" in r for r in results)
