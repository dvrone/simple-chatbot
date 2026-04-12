# 🤖 Simple Chatbot

An Uzbek-language chatbot built with Scikit-learn and Sentence Transformers.

## 🚀 Features

- 💬 Conversational AI in Uzbek language
- 🧠 Memory system (name, age, city)
- 🎵 Music player (play, stop, list)
- 🔊 Volume control
- 🕐 Real-time date and time
- 🔍 Fuzzy matching (understands typos)
- 🌑 Dark mode UI (Streamlit)

## 🛠️ Tech Stack

- Python 3.14
- scikit-learn
- sentence-transformers
- Streamlit
- thefuzz
- gTTS
- mpg123

## 📦 Installation

```bash
git clone https://github.com/dvrone/simple-chatbot.git
cd simple-chatbot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Usage

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
├── app.py              # Streamlit GUI
├── chatbot.py          # Terminal chatbot
├── data/
│   └── intents.json    # Intent data
├── models/             # Saved models
├── src/
│   ├── handlers.py     # Response handlers
│   ├── memory.py       # Memory system
│   ├── predictor.py    # Main predictor
│   ├── trainer.py      # Model trainer
│   └── utils.py        # Utility functions
└── requirements.txt
```

## 💬 Commands

| Command | Result |
| --------- | --------- |
| `salom` | Greeting |
| `mening ismim [name]` | Remember name |
| `yoshim [age]` | Remember age |
| `[city]da yashayman` | Remember city |
| `musiqa qo'y` | Play random music |
| `[song name] qo'y` | Play specific song |
| `musiqalar` | List all music |
| `stop` | Stop music |
| `ovozni oshir` | Volume up |
| `ovozni pasayt` | Volume down |
| `soat necha` | Current time |
| `bugun qaysi kun` | Current date |

## 📄 License

MIT
