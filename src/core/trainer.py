import pickle
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from src.core.utils import preprocess


class ChatbotTrainer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)
        self.classifier = LogisticRegression(max_iter=1000)

    def train(self, X: list, y: list):
        embeddings = self.encoder.encode(X)
        self.classifier.fit(embeddings, y)

    def save(self, path: str = "models/chatbot.pkl"):
        Path(path).parent.mkdir(exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({"encoder": self.encoder, "classifier": self.classifier}, f)
        print(f"Model saqlandi: {path}")
