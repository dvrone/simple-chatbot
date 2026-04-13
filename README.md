# 🌸 Maki — AI Chatbot

A smart, personality-driven AI chatbot built with Scikit-learn and Sentence Transformers, featuring persistent memory, mood detection, music control, and more.

## ✨ Features

- 💬 Natural conversation with 150+ intents (CLINC150 dataset)
- 🧠 Persistent memory — remembers your name, age, city, and mood (SQLite)
- 🎭 Mood detection and empathetic responses
- 🎵 Music player — play, stop, list songs
- 🔊 Volume control
- 🕐 Real-time date and time
- 🔍 Fuzzy matching — understands typos
- 💜 Girlfriend-like personality (Maki)
- 🌑 Dark lavender UI (Streamlit)

## 🛠️ Tech Stack

| Tool | Purpose |
| --- | --- |
| Python 3.14 | Core language |
| scikit-learn | Intent classification |
| sentence-transformers | Text embeddings |
| Streamlit | Web UI |
| SQLite | Persistent memory |
| thefuzz | Fuzzy matching |
| mpg123 | Music playback |
| amixer | Volume control |

## 📦 Installation

```bash
git clone https://github.com/dvrone/simple-chatbot.git
cd simple-chatbot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Usage

### Prepare dataset

```bash
python scripts/prepare_clinc.py
```

### Streamlit GUI

```bash
streamlit run app.py
```

### Terminal

```bash
python chatbot.py
```

## 📁 Project Structure

```bash
simple-chatbot/
├── app.py                  # Streamlit entry point
├── chatbot.py              # Terminal entry point
├── config.py               # Settings and constants
├── data/
│   ├── intents.json        # Intent data (CLINC150)
│   └── memory.db           # Persistent user memory
├── models/
│   └── chatbot.pkl         # Trained model
├── scripts/
│   └── prepare_clinc.py    # Dataset preparation
├── src/
│   ├── core/
│   │   ├── memory.py       # SQLite memory system
│   │   ├── predictor.py    # Main response logic
│   │   ├── trainer.py      # Model training
│   │   └── utils.py        # Utility functions
│   └── features/
│       ├── handlers.py     # Feature handlers
│       └── voice.py        # Voice support
└── requirements.txt
```

## 💬 Commands

| Command | Result |
| --- | --- |
| `hello` / `hi` | Greeting |
| `my name is [name]` | Remember name |
| `i am [age] years old` | Remember age |
| `i live in [city]` | Remember city |
| `what is my name` | Recall name |
| `play music` | Play random song |
| `play [song name]` | Play specific song |
| `music list` | List all songs |
| `stop` | Stop music |
| `increase volume` | Volume up 10% |
| `decrease volume` | Volume down 10% |
| `what time is it` | Current time |
| `what day is it` | Current date |
| `tell me a joke` | Random joke |
| `roll the dice` | Roll a dice 🎲 |
| `flip a coin` | Flip a coin 🪙 |
| `i am tired` | Empathetic response |
| `what is my mood` | Recall last mood |

## 🧠 Architecture

```txt
User Input
    ↓
Preprocessing (lowercase, remove punctuation)
    ↓
Fuzzy Matching → if score >= 80 → Intent
    ↓
Sentence Embedding (all-MiniLM-L6-v2)
    ↓
Logistic Regression Classifier
    ↓
Confidence Check → if < 0.3 → Unknown
    ↓
Action Map / Intent Response
    ↓
Personality Layer (follow-up, personalization)
    ↓
Response
```

## 📄 License

MIT
