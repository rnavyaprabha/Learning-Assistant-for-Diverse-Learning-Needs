# summarization.py

import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text: str, max_tokens: int = 150, temperature: float = 0.5) -> str:
    """
    Summarizes the provided text using OpenAI's ChatCompletion API.
    
    Parameters:
    - text (str): The text to be summarized.
    - max_tokens (int): The maximum length of the summary.
    - temperature (float): Temperature parameter for response creativity.
    
    Returns:
    - str: A concise summary of the text.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        summary = response.choices[0].message["content"].strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"

def summarize_notes():
    # Read the content of notes.txt
    with open("Summarization/notes.txt", "r") as file:
        notes_content = file.read()

    # Summarize the content
    summary = summarize_text(notes_content)
    print("Summary:\n", summary)

# Run the summarization when this file is executed
if __name__ == "__main__":
    summarize_notes()
