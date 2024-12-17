from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
load_dotenv()

def translate_text(text, target_language):
    # Create a client
    client = translate.Client()  

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]