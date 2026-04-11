from pathlib import Path

import streamlit as st

from src.predictor import ChatbotPredictor
from src.trainer import ChatbotTrainer
from src.utils import load_intents, prepare_data

INTENTS_PATH = "data/intents.json"
MODEL_PATH = "models/chatbot.pkl"

# Model yo'q bo'lsa o'rgat
if not Path(MODEL_PATH).exists():
    intents = load_intents(INTENTS_PATH)
    X, y = prepare_data(intents)
    trainer = ChatbotTrainer()
    trainer.train(X, y)
    trainer.save(MODEL_PATH)

# Intents yuklash
intents = load_intents(INTENTS_PATH)

# Predictor va xabarlarni session_state da saqlash
if "predictor" not in st.session_state:
    st.session_state.predictor = ChatbotPredictor(MODEL_PATH)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sahifa sozlamalari
st.set_page_config(page_title="ChatBot", page_icon="🤖")
st.title("🤖 ChatBot")

# Oldingi xabarlarni ko'rsatish
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if user_input := st.chat_input("Xabar yozing..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = st.session_state.predictor.get_response(user_input, intents)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
