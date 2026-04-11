import pickle
import random

from thefuzz import process

from src.memory import Memory
from src.utils import preprocess


class ChatbotPredictor:
    def __init__(self, model_path: str = "models/chatbot.pkl"):
        with open(model_path, "rb") as f:
            data = pickle.load(f)
        self.encoder = data["encoder"]
        self.classifier = data["classifier"]
        self.all_patterns = {}
        self.memory = Memory()

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

    def extract_user_data(self, text: str):
        text_lower = text.lower()
        triggers = ["ismim ", "mening ismim ", "meni chaqir "]
        for keyword in triggers:
            if keyword in text_lower:
                parts = text_lower.split(keyword)
                if len(parts) > 1:
                    name = parts[1].strip().split()[0].capitalize()
                    if name and name.lower() not in ["nima", "kim", "qanday"]:
                        self.memory.remember("name", name)

    def predict(self, text: str) -> str:
        text = preprocess(text)
        fuzzy_tag = self.fuzzy_match(text)
        if fuzzy_tag:
            return fuzzy_tag
        embedding = self.encoder.encode([text])
        return self.classifier.predict(embedding)[0]

    def get_response(self, text: str, intents: dict) -> str:
        if not self.all_patterns:
            self.load_patterns(intents)

        text_lower = text.lower()

        # 1. Avval ism so'rashni tekshirish
        if any(
            w in text_lower
            for w in ["ismim nima", "mening ismim nima", "meni bilasanmi"]
        ):
            name = self.memory.recall("name")
            if name:
                return f"Sizning ismingiz {name}!"
            return "Ismingizni bilmayman, aytib bering!"

        # 2. Keyin ism saqlash
        self.extract_user_data(text)
        if any(w in text_lower for w in ["ismim ", "mening ismim "]):
            name = self.memory.recall("name")
            if name:
                return f"Salom {name}, ismingizni eslab qoldim! 😊"

        # 3. Intent tekshirish
        tag = self.predict(text)
        self.memory.add("user", text)

        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                self.memory.add("bot", response)
                return response

        return "Tushunmadim, qaytadan yozing."
