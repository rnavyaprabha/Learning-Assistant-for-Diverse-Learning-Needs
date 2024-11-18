import sounddevice as sd
import numpy as np
import soundfile as sf
import asyncio
import aiohttp
import json
from transformers import pipeline

# Initialize Whisper model for file transcription
whisper_pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    chunk_length_s=30,
    device="cuda" if torch.cuda.is_available() else "cpu",
)

# Deepgram API settings
DEEPGRAM_API_KEY = "2de3e9345d70fc5f096c62a924744275a4920e67"  # Replace with your API key
sample_rate = 16000  # Deepgram requires 16 kHz for real-time transcription
channels = 1
chunk_duration = 5  # Duration of each chunk sent for transcription in seconds

# Real-time transcription with Deepgram
async def stream_audio():
    url = "wss://api.deepgram.com/v1/listen"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, headers=headers) as ws:
            print("Recording... Press Ctrl+C to stop.")

            # Stream audio data in real-time
            def audio_callback(indata, frames, time, status):
                if status:
                    print(f"Warning: {status}")
                # Send audio data in chunks to Deepgram
                asyncio.run_coroutine_threadsafe(ws.send_bytes(indata.tobytes()), asyncio.get_event_loop())

            # Start recording from microphone
            with sd.InputStream(samplerate=sample_rate, channels=channels, callback=audio_callback):
                try:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            # Extract and print the transcription text
                            if "channel" in data and "alternatives" in data["channel"]["alternatives"][0]:
                                transcription = data["channel"]["alternatives"][0]["transcript"]
                                if transcription:
                                    print("Real-time Transcription:", transcription)
                        elif msg.type == aiohttp.WSMsgType.CLOSE:
                            break
                except KeyboardInterrupt:
                    print("\nRecording stopped.")

# File-based transcription function
def file_transcription(file_path):
    try:
        audio_data, file_sample_rate = sf.read(file_path, dtype='float32')
        if file_sample_rate != sample_rate:
            raise ValueError("Audio file must be sampled at 16kHz")

        result = whisper_pipe({"array": audio_data, "sampling_rate": file_sample_rate})["text"]
        print(f"File Transcription: {result}")
    except Exception as e:
        print(f"Error in file transcription: {e}")

# Main program
def main():
    print("Select an option:")
    print("1: Real-time transcription from microphone")
    print("2: Transcription from an audio file")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        asyncio.run(stream_audio())
    elif choice == "2":
        file_path = input("Enter the path to the audio file: ")
        file_transcription(file_path)
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
