import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def correct_grammar(text: str, max_tokens: int = 1500, temperature: float = 0.5) -> str:
    """
    Corrects the grammar of the provided text using OpenAI's ChatCompletion API.
    
    Parameters:
    - text (str): The text to be corrected.
    - max_tokens (int): The maximum length of the corrected text.
    - temperature (float): Temperature parameter for response creativity.
    
    Returns:
    - str: The grammatically corrected text.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that corrects grammar."},
                {"role": "user", "content": f"Correct the grammar of the following text:\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        corrected_text = response.choices[0].message["content"].strip()
        return corrected_text
    except Exception as e:
        return f"Error correcting grammar: {e}"