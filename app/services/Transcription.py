from google.cloud import speech
from dotenv import load_dotenv
load_dotenv()

client = speech.SpeechAsyncClient()

async def transcribe_audio(websocket):

    # Google Speech-to-Text configuration
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        max_alternatives=1,
        enable_automatic_punctuation=True,  # Optional
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # Async generator to yield audio chunks
    async def audio_generator():
        print("Audio generator started...")
        speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        try:
            while True:
                audio_chunk = await websocket.receive_bytes()  # Wait for raw audio data
                print(f"Received audio chunk of size {len(audio_chunk)} bytes")
                if len(audio_chunk) > 0:
                    yield speech.RecognitionAudio(content=audio_chunk)
                else:
                    print("Received empty audio chunk!")
        except Exception as e:
            print(f"Audio generator stopped: {e}")
            return

    # Start streaming recognition
    try:
        print("Starting streaming recognition...")
        
        # Ensure the generator keeps yielding chunks
        responses = await client.streaming_recognize(requests=audio_generator())
        print("Streaming recognition initialized successfully...")

        # Process responses
        async for response in responses:
            print(f"Processing response: {response}")
            for result in response.results:
                if result.is_final:
                    print(f"Final transcript: {result.alternatives[0].transcript}")
                    yield {
                        "transcript": result.alternatives[0].transcript,
                        "is_final": True,
                    }
                else:
                    print(f"Partial transcript: {result.alternatives[0].transcript}")
                    yield {
                        "transcript": result.alternatives[0].transcript,
                        "is_final": False,
                    }
    except Exception as e:
        print(f"Error during transcription: {e}")
        yield {"error": str(e)}  # Send error back to client