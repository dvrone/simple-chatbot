import os
import pickle
import random
from datetime import datetime
from pathlib import Path

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

    def get_current_time(self) -> str:
        now = datetime.now()
        return f"Hozir soat {now.strftime('%H:%M')} 🕐"

    def get_current_date(self) -> str:
        now = datetime.now()
        days = [
            "Dushanba",
            "Seshanba",
            "Chorshanba",
            "Payshanba",
            "Juma",
            "Shanba",
            "Yakshanba",
        ]
        months = [
            "Yanvar",
            "Fevral",
            "Mart",
            "Aprel",
            "May",
            "Iyun",
            "Iyul",
            "Avgust",
            "Sentabr",
            "Oktabr",
            "Noyabr",
            "Dekabr",
        ]
        day_name = days[now.weekday()]
        month_name = months[now.month - 1]
        return f"Bugun {day_name}, {now.day} {month_name} {now.year} 📅"

    def get_music_list(self) -> list:
        music_dir = Path.home() / "Music"
        extensions = (".mp3", ".wav", ".flac", ".ogg")
        return [f for f in music_dir.iterdir() if f.suffix in extensions]

    def play_music(self, text: str) -> str:
        files = self.get_music_list()
        if not files:
            return "Musiqa papkasida hech narsa topilmadi!"

        text_lower = text.lower()
        for f in files:
            stem_normalized = f.stem.lower().replace("-", " ").replace("_", " ")
            if stem_normalized in text_lower or f.stem.lower() in text_lower:
                os.system(f"mpg123 '{f}' &")
                return f"🎵 {f.stem} ijro etilmoqda!"

        chosen = random.choice(files)
        os.system(f"mpg123 '{chosen}' &")
        return f"🎵 {chosen.stem} ijro etilmoqda!"

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

        # Ism so'rash
        if any(
            w in text_lower
            for w in ["ismim nima", "mening ismim nima", "meni bilasanmi"]
        ):
            name = self.memory.recall("name")
            if name:
                return f"Sizning ismingiz {name}!"
            return "Ismingizni bilmayman, aytib bering!"

        # Ism saqlash
        self.extract_user_data(text)
        if any(w in text_lower for w in ["ismim ", "mening ismim "]):
            name = self.memory.recall("name")
            if name:
                return f"Salom {name}, ismingizni eslab qoldim! 😊"

        # Musiqa to'xtatish
        if any(w in text_lower for w in ["stop", "to'xtat", "bas", "yetarli"]):
            os.system("pkill mpg123")
            return "🎵 Musiqa to'xtatildi!"

        # Musiqa ijro etish
        if any(w in text_lower for w in ["musiqa", "qo'shiq", "qo'y", "ijro"]):
            return self.play_music(text)

        # Vaqt
        if any(
            w in text_lower
            for w in ["soat necha", "soat nechada", "hozir soat", "vaqt"]
        ):
            return self.get_current_time()

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
            return self.get_current_date()

        # Intent tekshirish
        tag = self.predict(text)
        self.memory.add("user", text)

        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                self.memory.add("bot", response)
                return response

        return "Tushunmadim, qaytadan yozing."
