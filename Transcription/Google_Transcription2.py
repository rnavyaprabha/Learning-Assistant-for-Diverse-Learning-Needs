# transcription.py
from google.cloud import speech
from google.oauth2 import service_account
import pyaudio

# Set up Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file('C:\\Users\\vivas\\Documents\\PFW\\4-Fall 24\\Deep Learning\\Project\\proud-life-437323-r0-b54946475fce.json')
client = speech.SpeechClient(credentials=credentials)

# Audio parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Function to start the audio stream and handle transcription
async def transcribe_audio(websocket):
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    try:
        # Configure the audio stream for Google Cloud Speech API
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code="en-US",
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True
        )

        # Asynchronous generator to provide audio chunks to the API
        async def audio_generator():
            while True:
                audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
                yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)
        
        # Start the streaming recognition process
        responses = client.streaming_recognize(config=streaming_config, requests=audio_generator())

        # Process responses and send transcripts via WebSocket
        async for response in responses:
            for result in response.results:
                if result.is_final:
                    await websocket.send_json({"transcript": result.alternatives[0].transcript})
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        # Ensure the audio stream is closed
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()
