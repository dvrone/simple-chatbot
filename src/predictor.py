import pickle
import random
import re

from thefuzz import process

from src.handlers import (MemoryHandler, MusicHandler, PersonalityHandler,
                          TimeHandler, VolumeHandler)
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
        self.time = TimeHandler()
        self.music = MusicHandler()
        self.volume = VolumeHandler()
        self.mem_handler = MemoryHandler(self.memory)
        self.personality = PersonalityHandler(self.memory)

    def load_patterns(self, intents: dict):
        for intent in intents["intents"]:
            for pattern in intent["patterns"]:
                self.all_patterns[preprocess(pattern)] = intent["tag"]

    def fuzzy_match(self, text: str) -> str | None:
        if not self.all_patterns:
            return None
        match, score = process.extractOne(text, self.all_patterns.keys())
        if score >= 80:  # 70 dan 80 ga oshirdik
            return self.all_patterns[match]
        return None

    def predict(self, text: str) -> str | None:
        text = preprocess(text)
        fuzzy_tag = self.fuzzy_match(text)
        if fuzzy_tag:
            return fuzzy_tag
        embedding = self.encoder.encode([text])
        proba = self.classifier.predict_proba(embedding)[0]
        if max(proba) < 0.3:  # ishonch past bo'lsa None qaytaradi
            return None
        return self.classifier.predict(embedding)[0]

    def get_response(self, text: str, intents: dict) -> str:
        if not self.all_patterns:
            self.load_patterns(intents)

        text_lower = text.lower()

        # Salom
        if re.search(r"\b(salom|assalomu alaykum|hayy)\b", text_lower):
            return self.personality.greet()

        # Xayr
        if re.search(r"\b(xayr|hayr|ko'rishguncha|bye)\b", text_lower):
            return self.personality.farewell()

        # Ism so'rash
        if any(
            w in text_lower
            for w in ["ismim nima", "mening ismim nima", "meni bilasanmi"]
        ):
            return self.mem_handler.recall_name()

        # Yosh so'rash
        if any(w in text_lower for w in ["yoshim necha", "men necha yoshda"]) or (
            "yoshim" in text_lower and "?" in text
        ):
            return self.mem_handler.recall_age()

        # Shahar so'rash
        if any(
            w in text_lower
            for w in ["qayerda yashayman", "shahrim qayer", "qayerdanman"]
        ):
            return self.mem_handler.recall_city()

        # Ma'lumot saqlash
        self.mem_handler.extract(text)

        # Ism saqlash javobi
        if any(w in text_lower for w in ["ismim ", "mening ismim "]):
            name = self.memory.recall("name")
            if name:
                return f"Salom {name}, ismingizni eslab qoldim! 🌸"

        # Yosh saqlash javobi
        if "yoshim" in text_lower and "?" not in text:
            age = self.memory.recall("age")
            if age:
                return f"Yoshingiz {age} ekanini eslab qoldim! 💙"

        # Shahar saqlash javobi
        if any(w in text_lower for w in ["da yashayman", "dan kelganman"]):
            city = self.memory.recall("city")
            if city:
                return f"{city}da yashashingizni eslab qoldim! 🌸"

        # Musiqa ro'yxati
        if any(
            w in text_lower
            for w in ["musiqa ro'yxat", "qo'shiqlar", "musiqalar", "nima bor"]
        ):
            return self.music.show_list()

        # Ovoz balandligi
        if any(w in text_lower for w in ["ovozni oshir", "balandroq", "ovoz oshir"]):
            return self.volume.up()

        if any(w in text_lower for w in ["ovozni pasayt", "pastroq", "ovoz pasayt"]):
            return self.volume.down()

        # Musiqa to'xtatish
        if any(w in text_lower for w in ["stop", "to'xtat", "bas", "yetarli"]):
            return self.music.stop()

        # Musiqa ijro etish
        if any(w in text_lower for w in ["musiqa", "qo'shiq", "qo'y", "ijro"]):
            return self.music.play(text)

        # Vaqt
        if any(
            w in text_lower
            for w in ["soat necha", "soat nechada", "hozir soat", "vaqt"]
        ):
            return self.time.get_time()

        # Sana
        if any(
            w in text_lower
            for w in [
                "bugun necha",
                "bugun sana",
                "qaysi kun",
                "bugun kun",
                "kun necha",
                "sana",
            ]
        ):
            return self.time.get_date()

        # Intent tekshirish
        tag = self.predict(text)
        if tag is None:
            return self.personality.unknown()

        self.memory.add("user", text)

        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                self.memory.add("bot", response)
                return response

        return self.personality.unknown()
