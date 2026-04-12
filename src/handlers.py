import os
import random
from datetime import datetime
from pathlib import Path

from thefuzz import process

from src.memory import Memory


class PersonalityHandler:
    NAME = "Maki"
    STYLE = "muloyim"

    def __init__(self, memory: Memory):
        self.memory = memory

    def _get_name(self) -> str:
        name = self.memory.recall("name")
        return f" {name}" if name else ""

    def greet(self) -> str:
        name = self._get_name()
        options = [
            f"Salom{name}! Men Makiman, qanday yordam bera olaman? 🌸",
            f"Assalomu alaykum{name}! Maki shu yerda 💜",
            f"Xush kelibsiz{name}! 🌸",
        ]
        return random.choice(options)

    def farewell(self) -> str:
        name = self._get_name()
        options = [
            f"Xayr{name}! O'zingizni ezing 💜",
            f"Ko'rishguncha{name}! Sog' bo'ling 🌸",
            f"Ehtiyot bo'ling{name}! 💜",
        ]
        return random.choice(options)

    def unknown(self) -> str:
        name = self._get_name()
        options = [
            f"Tushunmadim{name}, qaytadan aytib bering 🥺",
            f"Kechirasiz{name}, bu haqda bilmayman 💜",
            f"Hmm{name}, aniqroq aytsangiz? 🌸",
        ]
        return random.choice(options)


class TimeHandler:
    def get_time(self) -> str:
        now = datetime.now()
        return f"Hozir soat {now.strftime('%H:%M')} 🕐"

    def get_date(self) -> str:
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

    def get_time_en(self) -> str:
        now = datetime.now()
        return f"It's {now.strftime('%H:%M')} 🕐"

    def get_date_en(self) -> str:
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')} 📅"


class MusicHandler:
    MUSIC_DIR = Path.home() / "Music"
    EXTENSIONS = (".mp3", ".wav", ".flac", ".ogg")

    def get_list(self) -> list:
        return [f for f in self.MUSIC_DIR.iterdir() if f.suffix in self.EXTENSIONS]

    def play(self, text: str) -> str:
        files = self.get_list()
        if not files:
            return "Musiqa papkasida hech narsa topilmadi!"

        os.system("pkill mpg123")
        stems = {f.stem.lower().replace("-", " ").replace("_", " "): f for f in files}
        match, score = process.extractOne(text.lower(), stems.keys())
        chosen = stems[match] if score >= 50 else random.choice(files)
        os.system(f"mpg123 '{chosen}' &")
        return f"🎵 {chosen.stem} ijro etilmoqda!"

    def stop(self) -> str:
        os.system("pkill mpg123")
        return "🎵 Musiqa to'xtatildi!"

    def show_list(self) -> str:
        files = self.get_list()
        if not files:
            return "Musiqa papkasida hech narsa topilmadi!"
        names = "\n".join([f"🎵 {f.stem}" for f in files])
        return f"Musiqa papkasidagi qo'shiqlar:\n{names}"


class VolumeHandler:
    def _get_volume(self) -> str:
        result = os.popen("amixer get Master").read()
        for line in result.split("\n"):
            if "Front Left:" in line:
                return line.split("[")[1].split("]")[0]
        return "?"

    def up(self) -> str:
        os.system("amixer set Master 10%+")
        return f"🔊 Ovoz balandligi: {self._get_volume()}"

    def down(self) -> str:
        os.system("amixer set Master 10%-")
        return f"🔉 Ovoz balandligi: {self._get_volume()}"


class MemoryHandler:
    def __init__(self, memory: Memory):
        self.memory = memory

    def extract(self, text: str):
        text_lower = text.lower()

        # Ism
        for keyword in ["ismim ", "mening ismim ", "meni chaqir "]:
            if keyword in text_lower:
                parts = text_lower.split(keyword)
                if len(parts) > 1:
                    name = parts[1].strip().split()[0].capitalize()
                    if name and name.lower() not in ["nima", "kim", "qanday"]:
                        self.memory.remember("name", name)

        # Yosh
        if "yoshim" in text_lower and "?" not in text_lower:
            for word in text_lower.split():
                cleaned = word.strip("da,. ")
                if cleaned.isdigit():
                    self.memory.remember("age", cleaned)

        # Shahar
        for keyword in ["da yashayman", "dan kelganman"]:
            if keyword in text_lower:
                parts = text_lower.split(keyword)
                if parts[0].strip():
                    city_raw = parts[0].strip().split()[-1]
                    if city_raw.endswith("da"):
                        city = city_raw[:-2].capitalize()
                    elif city_raw.endswith("dan"):
                        city = city_raw[:-3].capitalize()
                    else:
                        city = city_raw.capitalize()
                    if city:
                        self.memory.remember("city", city)

    def recall_name(self) -> str:
        name = self.memory.recall("name")
        return (
            f"Sizning ismingiz {name}!"
            if name
            else "Ismingizni bilmayman, aytib bering!"
        )

    def recall_age(self) -> str:
        age = self.memory.recall("age")
        return (
            f"Siz {age} yoshdasiz!" if age else "Yoshingizni bilmayman, aytib bering!"
        )

    def recall_city(self) -> str:
        city = self.memory.recall("city")
        return (
            f"Siz {city}da yashaysiz!"
            if city
            else "Shahringizni bilmayman, aytib bering!"
        )
