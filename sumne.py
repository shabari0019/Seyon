# main.py

from backend.search_and_describe import search_and_describe
from backend.tts import speak_text
import os

# Path to the test image
query_image_path = "queries/img.png"

# Step 1: Search for matches
results = search_and_describe(query_image_path, top_k=3)

# Step 2: Get top match
top_result = results[0]
title = top_result["title"]
description = top_result["description"]

print("\n🔍 Top Match:")
print(f"📌 Title: {title}")
print(f"📝 Description: {description}")

# Step 3: Generate audio (speak & save)
print("\n🔊 Speaking description...")
speak_text(description)

# Confirm path
#print(f"\n✅ Audio saved to: {audio_path}")