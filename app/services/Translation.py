from transformers import pipeline

# Define a function to load the appropriate translation model
def get_translator(target_language):
    models = {
        'es': "Helsinki-NLP/opus-mt-en-es",
        'hi': "Helsinki-NLP/opus-mt-en-hi",
        'fr': "Helsinki-NLP/opus-mt-en-fr",
        'de': "Helsinki-NLP/opus-mt-en-de",
        'zh': "Helsinki-NLP/opus-mt-en-zh",
        'ar': "Helsinki-NLP/opus-mt-en-ar",
        'ja': "Helsinki-NLP/opus-mt-en-jap",
        'en': "Helsinki-NLP/opus-mt-mul-en"
    }
    
    model_name = models.get(target_language.lower())
    
    if not model_name:
        raise ValueError(f"Translation model for '{target_language}' is not available.")
    
    return pipeline("translation", model=model_name)

def translate_text(text, target_language):
    """Translates text to language using a pre-trained model."""
    try:
        print(target_language)
        translator = get_translator(target_language)
        result = translator(text)
        return result[0]['translation_text']
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

# Example usage
input_text = "Hello, world!"  # Example English text
target_language = "German"  # Desired target language
translated_text = translate_text(input_text, target_language)

if translated_text:
    print(f"Original text: {input_text}")
    print(f"Translated text ({target_language}): {translated_text}")
