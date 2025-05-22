# backend/tts.py

import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # Speaking speed (default is ~200)
    engine.setProperty('volume', 1.0)  # Volume: 0.0 to 1.0
    engine.say(text)
    engine.runAndWait()

def save_speech_to_file(text, output_path="static/audio/output_audio.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    print(f"Saved audio to {output_path}")
    return output_path
