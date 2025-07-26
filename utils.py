import os
import json
from config import EXIT_COMMANDS
from textblob import TextBlob

def is_exit_command(msg):
    return msg.lower().strip() in EXIT_COMMANDS

def store_candidate_data(data, file_path="data/candidates.json"):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    try:
        with open(file_path, 'r') as f:
            existing = json.load(f)
    except json.JSONDecodeError:
        existing = []

    existing.append(data)

    with open(file_path, 'w') as f:
        json.dump(existing, f, indent=4)

def analyze_sentiment(text):
    if not text.strip():
        return 0.0
    return TextBlob(text).sentiment.polarity
