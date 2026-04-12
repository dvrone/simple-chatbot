from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# File paths
INTENTS_PATH = DATA_DIR / "intents.json"
MODEL_PATH = MODELS_DIR / "chatbot.pkl"
MEMORY_DB_PATH = DATA_DIR / "memory.db"

# Model settings
ENCODER_MODEL = "all-MiniLM-L6-v2"
FUZZY_THRESHOLD = 80
CONFIDENCE_THRESHOLD = 0.3

# Music settings
MUSIC_DIR = Path.home() / "Music"
MUSIC_EXTENSIONS = (".mp3", ".wav", ".flac", ".ogg")

# Personality settings
BOT_NAME = "Maki"
BOT_STYLE = "gentle"
