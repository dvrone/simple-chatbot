import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

def listen() -> str:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    try:
        with sr.Microphone(sample_rate=16000) as source:
            print("Tinglayapman...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
        text = recognizer.recognize_google(audio, language="uz-UZ")
        return text
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"API xato: {e}")
        return ""

def speak(text: str):
    tts = gTTS(text=text, lang="uz")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        os.system(f"mpg123 {f.name}")
        os.unlink(f.name)