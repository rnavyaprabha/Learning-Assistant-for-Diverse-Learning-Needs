# transcription.py
from google.cloud import speech
from google.oauth2 import service_account
import base64

# Set up Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(
    'C:\\Users\\vivas\\Documents\\PFW\\4-Fall 24\\Deep Learning\\Project\\proud-life-437323-r0-b54946475fce.json'
)
client = speech.SpeechClient(credentials=credentials)

# Function to handle transcription of incoming audio
async def transcribe_audio(websocket):
    try:
        # Configure the audio stream for Google Cloud Speech API
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,  # Ensure this matches the frontend's audio sample rate
            language_code="en-US",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True
        )

        async def audio_generator():
            while True:
                # Receive base64-encoded audio data from the WebSocket
                base64_audio = await websocket.receive_text()
                audio_chunk = base64.b64decode(base64_audio)
                yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)

        # Start the streaming recognition process
        responses = client.streaming_recognize(config=streaming_config, requests=audio_generator())

        # Process responses and send transcripts via WebSocket
        async for response in responses:
            for result in response.results:
                if result.is_final:
                    transcript = result.alternatives[0].transcript
                    await websocket.send_json({"transcript": transcript})

    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        print("WebSocket connection closed")
