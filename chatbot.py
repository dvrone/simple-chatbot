from pathlib import Path

from src.predictor import ChatbotPredictor
from src.trainer import ChatbotTrainer
from src.utils import load_intents, prepare_data

INTENTS_PATH = "data/intents.json"
MODEL_PATH = "models/chatbot.pkl"


def train():
    intents = load_intents(INTENTS_PATH)
    X, y = prepare_data(intents)
    trainer = ChatbotTrainer()
    trainer.train(X, y)
    trainer.save(MODEL_PATH)


def chat():
    intents = load_intents(INTENTS_PATH)
    predictor = ChatbotPredictor(MODEL_PATH)
    print("ChatBot ishga tushdi! Chiqish uchun 'quit' yozing.\n")
    while True:
        user_input = input("Siz: ")
        if user_input.lower() == "quit":
            print("Xayr!")
            break
        response = predictor.get_response(user_input, intents)
        print(f"Bot: {response}\n")


if __name__ == "__main__":
    if not Path(MODEL_PATH).exists():
        print("Model o'rgatilmoqda...")
        train()
    chat()
