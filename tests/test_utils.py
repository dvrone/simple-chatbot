import pytest

from src.core.utils import prepare_data, preprocess


class TestPreprocess:
    """Tests for the preprocess utility function."""

    def test_lowercase(self):
        """Should convert text to lowercase."""
        assert preprocess("HELLO WORLD") == "hello world"

    def test_remove_punctuation(self):
        """Should remove punctuation from text."""
        assert preprocess("hello!") == "hello"
        assert preprocess("what's up?") == "whats up"

    def test_strip_whitespace(self):
        """Should strip leading and trailing whitespace."""
        assert preprocess("  hello  ") == "hello"

    def test_combined(self):
        """Should handle combined cases."""
        assert preprocess("  Hello, World!  ") == "hello world"

    def test_empty_string(self):
        """Should handle empty string."""
        assert preprocess("") == ""


class TestPrepareData:
    """Tests for the prepare_data utility function."""

    def test_returns_lists(self):
        """Should return two lists."""
        intents = {
            "intents": [
                {"tag": "greeting", "patterns": ["hello", "hi"], "responses": ["Hi!"]},
            ]
        }
        X, y = prepare_data(intents)
        assert isinstance(X, list)
        assert isinstance(y, list)

    def test_correct_length(self):
        """Should return lists of equal length."""
        intents = {
            "intents": [
                {"tag": "greeting", "patterns": ["hello", "hi"], "responses": ["Hi!"]},
                {"tag": "goodbye", "patterns": ["bye"], "responses": ["Bye!"]},
            ]
        }
        X, y = prepare_data(intents)
        assert len(X) == 3
        assert len(y) == 3

    def test_correct_labels(self):
        """Should assign correct labels to patterns."""
        intents = {
            "intents": [
                {"tag": "greeting", "patterns": ["hello"], "responses": ["Hi!"]},
            ]
        }
        X, y = prepare_data(intents)
        assert y[0] == "greeting"

    def test_preprocessed_patterns(self):
        """Should preprocess patterns before returning."""
        intents = {
            "intents": [
                {"tag": "greeting", "patterns": ["Hello!"], "responses": ["Hi!"]},
            ]
        }
        X, y = prepare_data(intents)
        assert X[0] == "hello"
