import pickle
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression


class ChatbotTrainer:
    """Handles training and saving the chatbot model."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the sentence encoder and classifier."""
        self.encoder = SentenceTransformer(model_name)
        self.classifier = LogisticRegression(max_iter=1000)

    def train(self, X: list, y: list):
        """Encode patterns and train the classifier."""
        embeddings = self.encoder.encode(X)
        self.classifier.fit(embeddings, y)

    def save(self, path: str = "models/chatbot.pkl"):
        """Save the trained encoder and classifier to disk."""
        Path(path).parent.mkdir(exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(
                {
                    "encoder": self.encoder,
                    "classifier": self.classifier,
                },
                f,
            )
        print(f"Model saved: {path}")
