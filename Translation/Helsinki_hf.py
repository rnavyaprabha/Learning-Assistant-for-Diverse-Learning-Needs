import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# using HF_KEY to authenticate
headers = {"Authorization": "Bearer " + os.getenv("HF_KEY")}

# API endpoint for translation
def get_API_URL(target_language):
    return "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-"+ target_language.lower()

def translate_text(text, target_language):
    API_URL = get_API_URL(target_language)
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['translation_text']

# Example usage
input_text = "Hello, how are you?"  # Example English text
translated_text = translate_text(input_text, 'es')

if translated_text:
    print(f"Original text: {input_text}")
    print(f"Translated text: {translated_text}")