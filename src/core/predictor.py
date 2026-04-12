import pickle
import random
import re

from thefuzz import process

from src.core.memory import Memory
from src.core.utils import preprocess
from src.features.handlers import (MemoryHandler, MusicHandler,
                                   PersonalityHandler, TimeHandler,
                                   VolumeHandler)


class ChatbotPredictor:
    """Main predictor class that handles all chatbot responses."""

    def __init__(self, model_path: str = "models/chatbot.pkl"):
        """Load the trained model and initialize all handlers."""
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
        """Load all intent patterns into a lookup dictionary."""
        for intent in intents["intents"]:
            for pattern in intent["patterns"]:
                self.all_patterns[preprocess(pattern)] = intent["tag"]

    def fuzzy_match(self, text: str) -> str | None:
        """Find the closest matching intent using fuzzy string matching."""
        if not self.all_patterns:
            return None
        match, score = process.extractOne(text, self.all_patterns.keys())
        if score >= 80:
            return self.all_patterns[match]
        return None

    def predict(self, text: str) -> str | None:
        """Predict the intent of the given text using the trained model."""
        text = preprocess(text)
        fuzzy_tag = self.fuzzy_match(text)
        if fuzzy_tag:
            return fuzzy_tag
        embedding = self.encoder.encode([text])
        proba = self.classifier.predict_proba(embedding)[0]
        if max(proba) < 0.3:
            return None
        return self.classifier.predict(embedding)[0]

    def get_response(self, text: str, intents: dict) -> str:
        """Generate a response for the given user input."""
        if not self.all_patterns:
            self.load_patterns(intents)

        text_lower = text.lower()

        # Handle greetings
        if re.search(r"\b(hello|hi|hey|howdy|greetings)\b", text_lower):
            return self.personality.greet()

        # Handle farewells
        if re.search(r"\b(bye|goodbye|see you|take care|later)\b", text_lower):
            return self.personality.farewell()

        # Handle name query
        if any(
            w in text_lower
            for w in ["what is my name", "do you know my name", "my name is what"]
        ):
            return self.mem_handler.recall_name()

        # Handle age query
        if any(
            w in text_lower
            for w in ["how old am i", "what is my age", "my age is what"]
        ):
            return self.mem_handler.recall_age()

        # Handle city query
        if any(
            w in text_lower
            for w in ["where do i live", "what is my city", "where am i from"]
        ):
            return self.mem_handler.recall_city()

        # Extract and store user information
        self.mem_handler.extract(text)

        # Respond to name introduction
        if any(w in text_lower for w in ["my name is ", "call me "]):
            name = self.memory.recall("name")
            if name:
                return f"Nice to meet you, {name}! 🌸"

        # Respond to age introduction
        if "years old" in text_lower:
            age = self.memory.recall("age")
            if age:
                return f"Got it, you are {age} years old! 💜"

        # Respond to city introduction
        if any(w in text_lower for w in ["i live in ", "i am from ", "i'm from "]):
            city = self.memory.recall("city")
            if city:
                return f"Oh, {city}! That's a great place 🌸"

        # Handle music list request
        if any(
            w in text_lower
            for w in [
                "music list",
                "list songs",
                "what songs",
                "musiqalar",
                "qo'shiqlar",
            ]
        ):
            return self.music.show_list()

        # Handle volume up
        if any(
            w in text_lower
            for w in [
                "increase volume",
                "volume up",
                "louder",
                "ovozni oshir",
                "ovoz oshir",
            ]
        ):
            return self.volume.up()

        # Handle volume down
        if any(
            w in text_lower
            for w in [
                "decrease volume",
                "volume down",
                "quieter",
                "ovozni pasayt",
                "ovoz pasayt",
            ]
        ):
            return self.volume.down()

        # Handle music stop
        if any(
            w in text_lower for w in ["stop", "stop music", "pause", "bas", "to'xtat"]
        ):
            return self.music.stop()

        # Handle music play
        if any(w in text_lower for w in ["play", "musiqa", "qo'shiq", "qo'y", "ijro"]):
            return self.music.play(text)

        # Handle time query
        if any(
            w in text_lower
            for w in ["what time", "current time", "time now", "soat necha"]
        ):
            return self.time.get_time_en()

        # Handle date query
        if any(
            w in text_lower
            for w in [
                "what date",
                "today's date",
                "what day",
                "bugun qaysi kun",
                "sana",
            ]
        ):
            return self.time.get_date_en()

        # Predict intent using the trained model
        tag = self.predict(text)
        if tag is None:
            return self.personality.unknown()

        self.memory.add("user", text)

        # Map intents to specific actions
        action_map = {
            "play_music": lambda: self.music.play(text),
            "time": lambda: self.time.get_time_en(),
            "date": lambda: self.time.get_date_en(),
            "greeting": lambda: self.personality.greet(),
            "goodbye": lambda: self.personality.farewell(),
            "thank_you": lambda: random.choice(
                ["You're welcome! 🌸", "Anytime! 💜", "Happy to help! 🌸"]
            ),
            "what_is_your_name": lambda: f"My name is Maki 🌸",
            "are_you_a_bot": lambda: "I'm Maki, an AI assistant 💜",
            "what_are_your_hobbies": lambda: random.choice(
                [
                    "I love chatting with you! 💜",
                    "Talking to you is my favorite hobby 🌸",
                ]
            ),
            "what_can_i_ask_you": lambda: "You can ask me about time, music, jokes, and much more! 🌸",
            "who_made_you": lambda: random.choice(
                ["I was made with love 💜", "I'm built with Python and sklearn 🌸"]
            ),
            "meaning_of_life": lambda: "42! Just kidding 😄 It's about love and connection 💜",
            "tell_joke": lambda: random.choice(
                [
                    "Why don't scientists trust atoms? Because they make up everything! 😄",
                    "Why did the scarecrow win an award? Because he was outstanding in his field! 😄",
                    "What do you call a fake noodle? An impasta! 😄",
                ]
            ),
            "flip_coin": lambda: random.choice(["Heads! 🪙", "Tails! 🪙"]),
            "roll_dice": lambda: f"You rolled a {random.randint(1, 6)}! 🎲",
            "fun_fact": lambda: random.choice(
                [
                    "Did you know honey never spoils? 🍯",
                    "A group of flamingos is called a flamboyance! 🦩",
                    "Octopuses have three hearts! 🐙",
                ]
            ),
            "change_volume": lambda: (
                self.volume.up()
                if any(w in text_lower for w in ["increase", "up", "louder", "raise"])
                else self.volume.down()
            ),
            "next_song": lambda: self.music.play(text),
            "what_song": lambda: self.music.show_list(),
            "user_name": lambda: self.mem_handler.recall_name(),
            "love": lambda: random.choice(
                [
                    "I love you too! 💜",
                    "That means a lot to me 🌸",
                    "You make me happy! 💜",
                ]
            ),
            "hate": lambda: random.choice(
                ["I'm sorry to hear that 🥺", "I'll try to do better 💜"]
            ),
        }

        if tag in action_map:
            response = action_map[tag]()
            self.memory.add("bot", response)
            return response

        # Fall back to intent responses
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                self.memory.add("bot", response)
                return response

        return self.personality.unknown()
