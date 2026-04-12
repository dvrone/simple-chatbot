from pathlib import Path

from src.core.predictor import ChatbotPredictor
from src.core.trainer import ChatbotTrainer
from src.core.utils import load_intents, prepare_data

# File paths
INTENTS_PATH = "data/intents.json"
MODEL_PATH = "models/chatbot.pkl"


def train():
    """Train and save the chatbot model."""
    intents = load_intents(INTENTS_PATH)
    X, y = prepare_data(intents)
    trainer = ChatbotTrainer()
    trainer.train(X, y)
    trainer.save(MODEL_PATH)


def chat():
    """Start the terminal chat loop."""
    intents = load_intents(INTENTS_PATH)
    predictor = ChatbotPredictor(MODEL_PATH)
    print("Maki is ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye! 💜")
            break
        response = predictor.get_response(user_input, intents)
        print(f"Maki: {response}\n")


if __name__ == "__main__":
    if not Path(MODEL_PATH).exists():
        print("Training model...")
        train()
    chat()
