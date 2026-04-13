import os
import random
from datetime import datetime
from pathlib import Path

from thefuzz import process

from src.core.memory import Memory

# Mood keywords mapping
MOOD_MAP = {
    "happy": ["happy", "great", "amazing", "wonderful", "excited", "joyful", "good"],
    "sad": ["sad", "unhappy", "depressed", "down", "miserable", "crying"],
    "tired": ["tired", "exhausted", "sleepy", "drained", "worn out", "charchadim"],
    "angry": ["angry", "frustrated", "annoyed", "mad", "furious"],
    "anxious": ["anxious", "nervous", "worried", "stressed", "scared"],
    "bored": ["bored", "boredom", "nothing to do", "unentertained"],
}

MOOD_RESPONSES = {
    "happy": [
        "That's wonderful to hear! 🌸 Your happiness makes me happy too 💜",
        "Yay! I love when you're happy! 🌸",
    ],
    "sad": [
        "I'm sorry you're feeling sad 🥺 I'm here for you 💜",
        "It's okay to feel sad sometimes. I'm always here 🌸",
    ],
    "tired": [
        "You should get some rest 🥺 Take care of yourself 💜",
        "Don't forget to rest! You deserve it 🌸",
    ],
    "angry": [
        "Take a deep breath 💜 It will be okay 🌸",
        "I'm sorry you're frustrated 🥺 Want to talk about it? 💜",
    ],
    "anxious": [
        "Everything will be okay 💜 I'm right here with you 🌸",
        "Take it one step at a time 🥺 You've got this 💜",
    ],
    "bored": [
        "Let me cheer you up! Want to hear a joke? 😄 💜",
        "I'm here! Want to play a game or listen to music? 🌸",
    ],
}

# Random follow-up phrases added occasionally to responses
FOLLOW_UPS = [
    "By the way, how are you doing? 💜",
    "Hope you're having a great day! 🌸",
    "Is there anything else I can help with? 💜",
    "You're amazing, you know that? 🌸",
    "I'm always here for you 💜",
    "Don't forget to take care of yourself! 🌸",
    "Sending you good vibes! 💜",
]


class PersonalityHandler:
    """Handles Maki's personality and dynamic responses."""

    NAME = "Maki"
    STYLE = "gentle"

    def __init__(self, memory: Memory):
        self.memory = memory

    def _get_name(self) -> str:
        """Retrieve the user's name from memory."""
        name = self.memory.recall("name")
        return name if name else ""

    def greet(self) -> str:
        """Return a personalized greeting."""
        name = self._get_name()
        name_str = f" {name}" if name else ""
        options = [
            f"Hi{name_str}! I'm Maki, how can I help you? 🌸",
            f"Hello{name_str}! Maki here 💜",
            f"Hey{name_str}! What can I do for you? 🌸",
        ]
        return random.choice(options)

    def add_follow_up(self, response: str) -> str:
        """Occasionally append a random follow-up phrase to a response."""
        # Add follow-up every 4 messages on average
        if random.random() < 0.25:
            follow_up = random.choice(FOLLOW_UPS)
            return f"{response}\n\n_{follow_up}_"
        return response

    def farewell(self) -> str:
        """Return a personalized farewell message."""
        name = self._get_name()
        name_str = f" {name}" if name else ""
        options = [
            f"Goodbye{name_str}! Take care 💜",
            f"See you later{name_str}! 🌸",
            f"Bye{name_str}! Stay safe 💜",
        ]
        return random.choice(options)

    def unknown(self) -> str:
        """Return a response for unrecognized input."""
        name = self._get_name()
        name_str = f" {name}" if name else ""
        options = [
            f"I didn't get that{name_str}, could you rephrase? 🥺",
            f"Sorry{name_str}, I don't know about that yet 💜",
            f"Hmm{name_str}, can you be more specific? 🌸",
        ]
        return random.choice(options)


class TimeHandler:
    """Handles time and date related responses."""

    def get_time(self) -> str:
        """Return the current time in Uzbek format."""
        now = datetime.now()
        return f"Hozir soat {now.strftime('%H:%M')} 🕐"

    def get_time_en(self) -> str:
        """Return the current time in English format."""
        now = datetime.now()
        return f"It's {now.strftime('%H:%M')} 🕐"

    def get_date(self) -> str:
        """Return the current date in Uzbek format."""
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

    def get_date_en(self) -> str:
        """Return the current date in English format."""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')} 📅"


class MusicHandler:
    """Handles music playback, listing, and stopping."""

    MUSIC_DIR = Path.home() / "Music"
    EXTENSIONS = (".mp3", ".wav", ".flac", ".ogg")

    def get_list(self) -> list:
        """Return a list of music files from the music directory."""
        return [f for f in self.MUSIC_DIR.iterdir() if f.suffix in self.EXTENSIONS]

    def play(self, text: str) -> str:
        """Play a song matching the query or a random one."""
        files = self.get_list()
        if not files:
            return "No music found in the Music folder!"

        # Stop any currently playing music
        os.system("pkill mpg123")

        stems = {f.stem.lower().replace("-", " ").replace("_", " "): f for f in files}
        match, score = process.extractOne(text.lower(), stems.keys())
        chosen = stems[match] if score >= 50 else random.choice(files)
        os.system(f"mpg123 '{chosen}' &")
        return f"🎵 Now playing: {chosen.stem}"

    def stop(self) -> str:
        """Stop the currently playing music."""
        os.system("pkill mpg123")
        return "🎵 Music stopped!"

    def show_list(self) -> str:
        """Return a formatted list of available songs."""
        files = self.get_list()
        if not files:
            return "No music found in the Music folder!"
        names = "\n".join([f"🎵 {f.stem}" for f in files])
        return f"Available songs:\n{names}"


class VolumeHandler:
    """Handles system volume control."""

    def _get_volume(self) -> str:
        """Read the current master volume percentage."""
        result = os.popen("amixer get Master").read()
        for line in result.split("\n"):
            if "Front Left:" in line:
                return line.split("[")[1].split("]")[0]
        return "?"

    def up(self) -> str:
        """Increase the system volume by 10%."""
        os.system("amixer set Master 10%+")
        return f"🔊 Volume: {self._get_volume()}"

    def down(self) -> str:
        """Decrease the system volume by 10%."""
        os.system("amixer set Master 10%-")
        return f"🔉 Volume: {self._get_volume()}"


class MemoryHandler:
    """Handles extracting and recalling user information."""

    def __init__(self, memory: Memory):
        self.memory = memory

    def extract(self, text: str):
        """Extract and store user information from text."""
        text_lower = text.lower()

        # Extract and store user's name - remove "i am" trigger
        for keyword in ["my name is ", "call me "]:  # "i am " olib tashlandi
            if keyword in text_lower:
                parts = text_lower.split(keyword)
                if len(parts) > 1:
                    name = parts[1].strip().split()[0].capitalize()
                    if name and name.lower() not in [
                        "what",
                        "who",
                        "how",
                        "nima",
                        "kim",
                        "qanday",
                        "not",
                        "very",
                        "so",
                        "really",
                        "just",
                        "tired",
                        "happy",
                        "sad",
                        "angry",
                        "anxious",
                        "bored",
                    ]:
                        self.memory.remember("name", name)

        # Extract and store user's age
        if "i am" in text_lower and "years old" in text_lower:
            words = text_lower.split()
            for word in words:
                if word.isdigit():
                    self.memory.remember("age", word)

        # Extract and store user's city (Uzbek patterns)
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

        # Extract and store user's city (English patterns)
        for keyword in ["i live in ", "i am from ", "i'm from "]:
            if keyword in text_lower:
                parts = text_lower.split(keyword)
                if len(parts) > 1:
                    city = parts[1].strip().split()[0].capitalize()
                    if city:
                        self.memory.remember("city", city)

    def detect_mood(self, text: str) -> str | None:
        """Detect the user's mood from the input text."""
        text_lower = text.lower()
        for mood, keywords in MOOD_MAP.items():
            if any(keyword in text_lower for keyword in keywords):
                return mood
        return None

    def handle_mood(self, text: str) -> str | None:
        """Detect, store, and respond to the user's mood."""
        # Skip negations
        if any(w in text.lower() for w in ["not ", "don't ", "doesn't ", "never "]):
            return None
        mood = self.detect_mood(text)
        if mood:
            self.memory.remember_mood(mood)
            responses = MOOD_RESPONSES.get(mood, [])
            if responses:
                return random.choice(responses)
        return None

    def recall_mood_response(self) -> str:
        """Return a response based on the last stored mood."""
        mood = self.memory.recall_last_mood()
        if not mood:
            return "I don't know how you're feeling yet, tell me! 🌸"
        responses = MOOD_RESPONSES.get(mood, [])
        if responses:
            return f"Last time you were feeling {mood}. {random.choice(responses)}"
        return f"Last time you were feeling {mood} 💜"

    def recall_name(self) -> str:
        """Return the user's stored name."""
        name = self.memory.recall("name")
        return (
            f"Your name is {name}!"
            if name
            else "I don't know your name yet, please tell me!"
        )

    def recall_age(self) -> str:
        """Return the user's stored age."""
        age = self.memory.recall("age")
        return (
            f"You are {age} years old!"
            if age
            else "I don't know your age yet, please tell me!"
        )

    def recall_city(self) -> str:
        """Return the user's stored city."""
        city = self.memory.recall("city")
        return (
            f"You live in {city}!"
            if city
            else "I don't know your city yet, please tell me!"
        )
