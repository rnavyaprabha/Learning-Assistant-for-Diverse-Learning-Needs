import torch
import numpy as np
import sounddevice as sd
import soundfile as sf
from transformers import pipeline

# Set up device for model processing (GPU/CPU)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Initialize Whisper pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    chunk_length_s=30,
    device=device,
)

# Audio capture parameters
sample_rate = 16000  # Required sample rate for Whisper
channels = 1  # Mono audio for transcription
frames_per_buffer = 1024  # Buffer size for real-time capture
audio_buffer = np.zeros(0, dtype=np.float32)  # Initialize buffer

# Microphone audio callback function
def audio_callback(indata, frames, time, status):
    global audio_buffer
    if status:
        print(status)

    # Append new audio data to the buffer
    audio_chunk = indata[:, 0].astype(np.float32)
    audio_buffer = np.append(audio_buffer, audio_chunk)

    # Process if buffer has enough data
    if len(audio_buffer) >= sample_rate * 5:  # Process every 5 seconds
        audio_data = {"array": audio_buffer[:sample_rate * 5], "sampling_rate": sample_rate}
        try:
            result = pipe(audio_data, batch_size=8)["text"]
            print(f"Transcription: {result}")
        except Exception as e:
            print(f"Error during transcription: {e}")

        # Clear the processed buffer
        audio_buffer = audio_buffer[sample_rate * 5:]

# Function for real-time microphone transcription
def real_time_transcription():
    # Query available devices
    devices = sd.query_devices()
    print("Available audio devices:", devices)

    # Select input device if available
    input_device_index = 0 if devices else None
    if input_device_index is None:
        print("No audio input devices found.")
        return

    # Start audio stream
    try:
        with sd.InputStream(samplerate=sample_rate, channels=channels,
                            callback=audio_callback, blocksize=frames_per_buffer,
                            device=input_device_index):
            print("Recording... Press Ctrl+C to stop.")
            while True:
                pass  # Keep stream open
    except sd.PortAudioError as e:
        print(f"Error opening audio stream: {e}")

# Function for file-based transcription
def file_transcription(file_path):
    try:
        # Load and verify audio file
        audio_data, file_sample_rate = sf.read(file_path, dtype='float32')
        if file_sample_rate != sample_rate:
            raise ValueError("Audio file sample rate must be 16kHz")

        # Transcribe
        result = pipe({"array": audio_data, "sampling_rate": sample_rate})["text"]
        print(f"Transcription: {result}")
    except Exception as e:
        print(f"Error loading or transcribing audio file: {e}")

# Main program
def main():
    print("Select an option:")
    print("1: Transcribe from microphone")
    print("2: Transcribe from an audio file")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        real_time_transcription()
    elif choice == "2":
        file_path = input("Enter the path to the audio file: ")
        file_transcription(file_path)
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
