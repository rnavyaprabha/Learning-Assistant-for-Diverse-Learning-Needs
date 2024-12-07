
import subprocess
import sys

# Install necessary packages if they aren't already installed
def install_packages():
    try:
        import transformers
        import sentencepiece
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers", "sentencepiece"])

install_packages()

from transformers import pipeline

# Load the translation pipeline
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")

def translate_to_english(text):
    """Translates text to English using a pre-trained model."""
    try:
        result = translator(text)
        return result[0]['translation_text']
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

# Example usage
input_text = "Bonjour le monde"  # Example French text
translated_text = translate_to_english(input_text)

if translated_text:
    print(f"Original text: {input_text}")
    print(f"Translated text: {translated_text}")
