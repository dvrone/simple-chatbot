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

    def _get_last_bot_message(self) -> str | None:
        """Return the last message sent by the bot."""
        for msg in reversed(self.memory.history):
            if msg["role"] == "bot":
                return msg["text"]
        return None

    def _get_last_user_message(self) -> str | None:
        """Return the second to last message sent by the user."""
        user_messages = [m for m in self.memory.history if m["role"] == "user"]
        if len(user_messages) >= 2:
            return user_messages[-2]["text"]
        return None

    def get_response(self, text: str, intents: dict) -> str:
        """Generate a response for the given user input."""
        if not self.all_patterns:
            self.load_patterns(intents)

        text_lower = text.lower()

        # Handle greetings - strict word boundary
        if re.search(r"\b(hello|hi|hey|howdy|greetings)\b", text_lower) and not any(
            w in text_lower
            for w in ["while", "their", "like", "this", "think", "within"]
        ):
            return self.personality.greet()

        # Handle farewells
        if re.search(r"\b(bye|goodbye|see you|take care|later)\b", text_lower):
            return self.personality.farewell()

        # Handle repeat request
        if any(w in text_lower for w in ["what did you say", "repeat", "say again"]):
            last_bot = self._get_last_bot_message()
            if last_bot:
                return f"I said: {last_bot} 🌸"
            return "I haven't said anything yet! 💜"

        # Handle context-aware follow-up questions
        last_bot = self._get_last_bot_message()
        last_user = self._get_last_user_message()

        if last_bot and any(
            w in text_lower for w in ["do you like it", "is it good", "how is it"]
        ):
            if "now playing" in last_bot.lower():
                song = last_bot.split(":")[-1].strip()
                return f"I love {song}! Great choice 🌸"

        if last_user and any(w in text_lower for w in ["why", "why so", "why not"]):
            mood = self.mem_handler.detect_mood(last_user)
            if mood:
                return (
                    f"Because you said you're feeling {mood} 🥺 I just want to help 💜"
                )

        if last_bot and any(
            w in text_lower for w in ["tell me more", "more", "continue"]
        ):
            return f"I said: '{last_bot}' 💜 Want to know more? 🌸"

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

        # Handle mood query
        if any(
            w in text_lower
            for w in ["how am i feeling", "what is my mood", "my last mood"]
        ):
            return self.mem_handler.recall_mood_response()

        # Extract and store user information
        self.mem_handler.extract(text)

        # Detect and handle mood
        mood_response = self.mem_handler.handle_mood(text)
        if mood_response:
            return mood_response

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
            "what_is_your_name": lambda: "My name is Maki 🌸",
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
            return response

        # Fall back to intent responses
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                return response

        return self.personality.unknown()
