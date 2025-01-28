import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# using HF_KEY to authenticate
headers = {"Authorization": "Bearer " + os.getenv("HF_KEY")}

# Translation models
translators = {
    'es': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-es",
    'hi': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-hi",
    'fr': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr",
    'de': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-de",
    'zh': "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-zh"
    # 'ar': https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ar,
    # 'ja': https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-jap,
    # 'en': https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-mul-en
}

# API endpoint for translation
def get_API_URL(target_language):
    return "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-"+ target_language.lower()

def translate_text(text, target_language):
    API_URL = get_API_URL(target_language)
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['translation_text']

# from google.cloud import translate_v2 as translate

# def translate_text(text, target_language):
#     # Create a client
#     client = translate.Client()  

#     if isinstance(text, bytes):
#         text = text.decode("utf-8")

#     result = client.translate(text, target_language=target_language)

#     return result["translatedText"]