import torch
import numpy as np
import sounddevice as sd
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Wav2Vec2 model and processor for real-time transcription
wav2vec2_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h").to(device)
wav2vec2_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")

# Whisper pipeline for file-based transcription
whisper_pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    chunk_length_s=30,
    device=device,
)

# Audio capture parameters
sample_rate = 16000  # Required by Wav2Vec2
channels = 1
chunk_duration = 5  # Chunk duration for real-time capture in seconds
frames_per_buffer = 1024
audio_buffer = np.zeros(0, dtype=np.float32)

# Callback function for capturing real-time audio
def audio_callback(indata, frames, time, status):
    global audio_buffer
    if status:
        print(f"Warning: {status}")
    audio_buffer = np.append(audio_buffer, indata[:, 0])

    # Process audio in chunks for transcription
    if len(audio_buffer) >= sample_rate * chunk_duration:
        # Preprocess and send to the model
        input_values = wav2vec2_processor(
            audio_buffer[:sample_rate * chunk_duration], sampling_rate=sample_rate, return_tensors="pt"
        ).input_values.to(device)
        
        with torch.no_grad():
            logits = wav2vec2_model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = wav2vec2_processor.batch_decode(predicted_ids)[0]
            print(f"Real-time Transcription: {transcription}")

        # Clear the buffer
        audio_buffer = audio_buffer[sample_rate * chunk_duration:]

# Real-time microphone transcription
def real_time_transcription():
    # Check available audio devices
    devices = sd.query_devices()
    print("Available audio devices:", devices)
    
    # Start audio stream
    try:
        with sd.InputStream(samplerate=sample_rate, channels=channels, callback=audio_callback):
            print("Recording... Press Ctrl+C to stop.")
            sd.sleep(10000)  # 10 seconds, adjust as needed
    except Exception as e:
        print(f"Error in real-time transcription: {e}")
    except KeyboardInterrupt:
        print("\nRecording stopped by user.")

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

# Main function
def main():
    print("Select an option:")
    print("1: Real-time transcription from microphone")
    print("2: Transcription from an audio file")
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
