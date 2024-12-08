from deepgram import Deepgram
import pyaudio
import asyncio
import threading

# Deepgram API key
DEEPGRAM_API_KEY = "2de3e9345d70fc5f096c62a924744275a4920e67"

# Audio parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Initialize the Deepgram client
dg_client = Deepgram(DEEPGRAM_API_KEY)

# Asynchronous transcription using Deepgram
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
        # Configure the Deepgram live transcription connection
        async with dg_client.transcription.live(
            {
                "punctuate": True,  # Adds punctuation to the transcription
                "interim_results": True,  # Provides interim results
                "language": "en-US",  # Set language to English
            }
        ) as deepgram_socket:
            print("Connected to Deepgram.")

            async def send_audio():
                """Send audio data to Deepgram."""
                while True:
                    # Read audio data from the microphone
                    audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
                    await deepgram_socket.send(audio_chunk)

            # Start sending audio to Deepgram in the background
            send_task = asyncio.create_task(send_audio())

            # Process responses from Deepgram
            async for response in deepgram_socket:
                if response.get("channel") and response["channel"].get("alternatives"):
                    transcription = response["channel"]["alternatives"][0]["transcript"]
                    print(f"Transcription: {transcription}")

                    # Send the transcription via WebSocket
                    await websocket.send_json({"transcript": transcription})

            # Ensure the sending task completes
            await send_task
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        # Ensure the audio stream is closed
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()
