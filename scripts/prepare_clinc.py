import json

from datasets import load_dataset


def prepare_clinc():
    print("CLINC150 yuklanmoqda...")
    ds = load_dataset("clinc_oos", "plus")

    label_names = ds["train"].features["intent"].names
    intents = {}

    for example in ds["train"]:
        label = label_names[example["intent"]]
        if label == "oos":  # out-of-scope skip
            continue
        if label not in intents:
            intents[label] = {"tag": label, "patterns": [], "responses": []}
        intents[label]["patterns"].append(example["text"])

    # Har intent uchun default response
    default_responses = {
        "greeting": [
            "Hello! I'm Maki, how can I help you? 🌸",
            "Hi there! Maki here 💜",
        ],
        "goodbye": ["Goodbye! Take care 💜", "See you later! 🌸"],
        "thank_you": ["You're welcome! 🌸", "Anytime! 💜"],
        "what_is_your_name": ["My name is Maki 🌸", "I'm Maki, your assistant 💜"],
        "are_you_a_bot": [
            "I'm Maki, an AI assistant 💜",
            "Yes, I'm an AI, but I care about you! 🌸",
        ],
        "what_can_i_ask_you": [
            "You can ask me about weather, music, time, and more! 🌸"
        ],
        "who_made_you": [
            "I was made with love 💜",
            "I'm Maki, built with Python and sklearn 🌸",
        ],
        "meaning_of_life": ["42! Just kidding 😄 It's about love and connection 💜"],
        "tell_joke": [
            "Why don't scientists trust atoms? Because they make up everything! 😄"
        ],
        "play_music": ["Playing music for you 🎵", "Sure, let me play something 🎶"],
        "time": ["Let me check the time for you 🕐"],
        "date": ["Let me check today's date 📅"],
        "weather": ["I can't check weather right now, but it looks nice outside! ☀️"],
        "calculator": ["I can't calculate that yet, try a calculator app 😊"],
        "timer": ["I can't set timers yet 🥺"],
        "alarm": ["I can't set alarms yet 🥺"],
        "flip_coin": ["Heads! 🪙", "Tails! 🪙"],
        "roll_dice": ["You rolled a 4! 🎲", "You rolled a 6! 🎲"],
        "fun_fact": [
            "Did you know honey never spoils? 🍯",
            "A group of flamingos is called a flamboyance! 🦩",
        ],
        "what_are_your_hobbies": [
            "I love chatting with you! 💜",
            "Talking to you is my favorite hobby 🌸",
        ],
    }

    extra_patterns = {
        "greeting": ["hello", "hi", "hey", "good morning", "good evening", "howdy"],
        "goodbye": ["bye", "goodbye", "see you", "take care", "later"],
        "thank_you": ["thanks", "thank you", "thx", "many thanks"],
        "translate": [
            "translate this",
            "how do you say in",
            "say it in french",
            "say it in spanish",
        ],
    }

    # Qo'shimcha custom intentlar
    custom_intents = [
        {
            "tag": "love",
            "patterns": [
                "i love you",
                "i like you",
                "you are great",
                "you're amazing",
                "i adore you",
            ],
            "responses": [
                "I love you too! 💜",
                "That means a lot to me 🌸",
                "You make me happy! 💜",
            ],
        },
        {
            "tag": "hate",
            "patterns": [
                "i hate you",
                "you are stupid",
                "you're useless",
                "i don't like you",
            ],
            "responses": ["I'm sorry to hear that 🥺", "I'll try to do better 💜"],
        },
    ]

    for custom in custom_intents:
        intents[custom["tag"]] = custom

    for tag, patterns in extra_patterns.items():
        if tag in intents:
            intents[tag]["patterns"].extend(patterns)

    for tag, intent in intents.items():
        if tag in default_responses:
            intent["responses"] = default_responses[tag]
        else:
            intent["responses"] = [f"I can help you with {tag.replace('_', ' ')}! 💜"]

    result = {"intents": list(intents.values())}

    with open("data/intents.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(intents)} ta intent saqlandi → data/intents.json")


if __name__ == "__main__":
    prepare_clinc()
