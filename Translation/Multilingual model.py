from transformers import pipeline

# Preload the translation models
translators = {
    'es': pipeline("translation", model="Helsinki-NLP/opus-mt-en-es"),
    'hi': pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi"),
    'fr': pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr"),
    'de': pipeline("translation", model="Helsinki-NLP/opus-mt-en-de"),
    'zh': pipeline("translation", model="Helsinki-NLP/opus-mt-en-zh")
    # 'ar': pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar"),
    # 'ja': pipeline("translation", model="Helsinki-NLP/opus-mt-en-jap"),
    # 'en': pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
}

def translate_text(text, target_language):
    """Translates text to the target language using preloaded models."""
    try:
        translator = translators.get(target_language.lower())
        if not translator:
            raise ValueError(f"Translation model for '{target_language}' is not available.")
        result = translator(text)
        return result[0]['translation_text']
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

# Example usage
input_text = "Bonjour le monde"  # Example French text
translated_text = translate_text(input_text, 'en')

if translated_text:
    print(f"Original text: {input_text}")
    print(f"Translated text: {translated_text}")