import json
import re

def load_intents(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = text.strip()
    return text

def prepare_data(intents: dict) -> tuple[list, list]:
    X, y = [], []
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            X.append(preprocess(pattern))
            y.append(intent["tag"])
    return X, y