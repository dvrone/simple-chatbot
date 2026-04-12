from pathlib import Path

import streamlit as st

from src.core.predictor import ChatbotPredictor
from src.core.trainer import ChatbotTrainer
from src.core.utils import load_intents, prepare_data

# File paths
INTENTS_PATH = "data/intents.json"
MODEL_PATH = "models/chatbot.pkl"

# Train the model if it doesn't exist
if not Path(MODEL_PATH).exists():
    intents = load_intents(INTENTS_PATH)
    X, y = prepare_data(intents)
    trainer = ChatbotTrainer()
    trainer.train(X, y)
    trainer.save(MODEL_PATH)

# Load intents and initialize predictor
intents = load_intents(INTENTS_PATH)

if "predictor" not in st.session_state:
    st.session_state.predictor = ChatbotPredictor(MODEL_PATH)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(page_title="Maki 💜", page_icon="🌸")
st.title("🌸 Maki")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = st.session_state.predictor.get_response(user_input, intents)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
