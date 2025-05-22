

# cli_main.py
from backend.search_and_describe import search_and_describe
from backend.tts import save_speech_to_file
import os
from time import sleep

def display_results(results):
    print("\n🔍 Top Matches:\n")
    for i, res in enumerate(results):
        print(f"{i+1}. {res['title']}")
        print(f"   {res['description']}\n")

def main():
    print("📸 Tourist Visual Guide – CLI Mode")
    image_path = input("Enter path to your query image (e.g., queries/img1.png): ").strip()

    if not os.path.exists(image_path):
        print("❌ Error: File not found.")
        return

    print("\n🧠 Searching for matches...")
    results = search_and_describe(image_path)

    display_results(results)

    # Speak the top result
    top_description = results[0]["description"]
    print("🔊 Generating audio...")
    audio_path = save_speech_to_file(top_description)

    # Ask if user wants to play audio
    play = input("▶️ Play the description out loud? (y/n): ").lower()
    if play == 'y':
        try:
            print("🔈 Playing audio...")
            if os.name == 'nt':
                os.system(f'start {audio_path}')  # Windows
            elif os.name == 'posix':
                os.system(f'afplay {audio_path}' if 'darwin' in os.sys.platform else f'mpg123 {audio_path}')
            sleep(3)
        except Exception as e:
            print("⚠️ Could not play audio. You can manually open:", audio_path)

if __name__ == "__main__":
    main()

