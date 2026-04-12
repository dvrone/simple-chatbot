import json
import re


def load_intents(path: str) -> dict:
    """Load intents from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def preprocess(text: str) -> str:
    """Normalize text: lowercase, remove punctuation, strip whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.strip()
    return text


def prepare_data(intents: dict) -> tuple[list, list]:
    """Extract patterns and labels from intents dictionary."""
    X, y = [], []
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            X.append(preprocess(pattern))
            y.append(intent["tag"])
    return X, y
