import pickle
import random
from thefuzz import process
from src.utils import preprocess

class ChatbotPredictor:
    def __init__(self, model_path: str = "models/chatbot.pkl"):
        with open(model_path, "rb") as f:
            data = pickle.load(f)
        self.encoder = data["encoder"]
        self.classifier = data["classifier"]
        self.all_patterns = {}

    def load_patterns(self, intents: dict):
        for intent in intents["intents"]:
            for pattern in intent["patterns"]:
                self.all_patterns[preprocess(pattern)] = intent["tag"]

    def fuzzy_match(self, text: str) -> str | None:
        if not self.all_patterns:
            return None
        match, score = process.extractOne(text, self.all_patterns.keys())
        if score >= 70:
            return self.all_patterns[match]
        return None

    def predict(self, text: str) -> str:
        text = preprocess(text)
        # Avval fuzzy match sinash
        fuzzy_tag = self.fuzzy_match(text)
        if fuzzy_tag:
            return fuzzy_tag
        # Keyin model
        embedding = self.encoder.encode([text])
        return self.classifier.predict(embedding)[0]

    def get_response(self, text: str, intents: dict) -> str:
        if not self.all_patterns:
            self.load_patterns(intents)
        tag = self.predict(text)
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
        return "Tushunmadim, qaytadan yozing."