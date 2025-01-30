import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# using HF_KEY to authenticate
headers = {"Authorization": "Bearer " + os.getenv("HF_KEY")}

# API endpoint for translation
def get_API_URL(target_language):
    return f"https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-{target_language.lower()}"

def translate_text(text, target_language, retries=4, delay=5):
    API_URL = get_API_URL(target_language)
    payload = {"inputs": text}

    for attempt in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload)

        # Handle potential issues in response
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.json()}")
            time.sleep(delay)  # Wait before retrying
            continue

        try:
            result = response.json()
            if isinstance(result, list) and "translation_text" in result[0]:
                return result[0]['translation_text']
            else:
                print(f"Unexpected response format: {result}")
        except Exception as e:
            print(f"JSON parsing error: {e}")
        
        time.sleep(delay)  # Wait before retrying

    return "Translation failed. Please try again later."
