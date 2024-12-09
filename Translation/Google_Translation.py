from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
load_dotenv()

def translate_text(text, target_language):
    # Create a client
    client = translate.Client()  

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result

if __name__ == "__main__":
    translate_text("Hello, how are you?", "es")