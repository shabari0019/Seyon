import pyttsx3

from backend.utils import get_abs_path
AUDIO_PATH = get_abs_path("../static/audio/current_audio.mp3")
print(AUDIO_PATH)
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # Speaking speed (default is ~200)
    engine.setProperty('volume', 1.0)  # Volume: 0.0 to 1.0
    engine.say(text)
    engine.runAndWait()




def generate_audio(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.save_to_file(text, AUDIO_PATH)
    engine.runAndWait()
    print(f"✅ Audio saved to {AUDIO_PATH}")
    return AUDIO_PATH
