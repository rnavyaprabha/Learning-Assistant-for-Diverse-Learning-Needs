
from google.cloud import speech
from google.oauth2 import service_account
import pyaudio

# Set up Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file('C:\\Users\\vivas\\Documents\\PFW\\4-Fall 24\\Deep Learning\\Project\\proud-life-437323-r0-b54946475fce.json')
client = speech.SpeechClient(credentials=credentials)

# Audio parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def record_audio():
    #Generator that yields audio chunks from the microphone
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    print("Recording...")

    try:
        while True:
            audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
            yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)
    except KeyboardInterrupt:
        print("Recording stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()

def transcribe_streaming():
    #Transcribes audio from the microphone in real time
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True  # Set to True for real-time partial results
    )

    # Use streaming_recognize with the audio generator
    responses = client.streaming_recognize(config=streaming_config, requests=record_audio())

    try:
        for response in responses:
            # Iterate through results in the response
            for result in response.results:
                if result.is_final:
                    print("Transcript: {}".format(result.alternatives[0].transcript))
                else:
                    print("Partial transcript: {}".format(result.alternatives[0].transcript))
    except Exception as e:
        print(f"Error during transcription: {e}")

if __name__ == "__main__":
    transcribe_streaming()