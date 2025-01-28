import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer " + os.getenv("HF_KEY")}

def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['summary_text']

# Example usage
input_text = "Facebook is an American online social media and social networking service company based in Menlo Park, California. Its website was launched on February 4, 2004, by Mark Zuckerberg, along with fellow Harvard College students and roommates Eduardo Saverin, Andrew McCollum, Dustin Moskovitz, and Chris Hughes."
summary = summarize_text(input_text)

if summary:
    print(f"Original text: {input_text}")
    print(f"Summary  text: {summary}")