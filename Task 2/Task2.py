# enhance_games.py
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# 1. Load API key from .env
load_dotenv()  
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API Key not found.")

# Google AI Studio API endpoint
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"


# 2. Function to call Google AI Studio API
def call_api(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print("API Error:", e)
        return "Unknown"

# 3. Prompt functions
def classify_genre(title):
    prompt = f"Classify the video game '{title}' into ONE single-word genre only. Example: Shooter, RPG, Sports, Strategy."
    return call_api(prompt)

def generate_description(title):
    prompt = f"Write a short description under 30 words for the video game '{title}'."
    return call_api(prompt)

def get_player_mode(title):
    prompt = f"Determine the player mode for the game '{title}'. Answer only with one of these: Singleplayer, Multiplayer, Both."
    return call_api(prompt)

# 4. Load CSV
df = pd.read_csv("Game Thumbnail.csv")

# 5. Enrich dataset with new columns
df["genre"] = df["game_title"].apply(classify_genre)
df["short_description"] = df["game_title"].apply(generate_description)
df["player_mode"] = df["game_title"].apply(get_player_mode)

# 6. Save to new CSV
output_file = "Game_Thumbnail_Enhanced.csv"
df.to_csv(output_file, index=False)
print(f"✅ Enhanced CSV saved as {output_file}")
