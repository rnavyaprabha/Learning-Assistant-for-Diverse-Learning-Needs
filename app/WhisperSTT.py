import sounddevice as sd
import whisper
import numpy as np

# Load Whisper model (Tiny or Base for real-time performance)
try:
    model = whisper.load_model("tiny")
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Define parameters
sample_rate = 16000  # Sample rate (16 kHz)
channels = 1         # Mono channel
frames_per_buffer = 1024  # Buffer size

# Callback function to process audio data
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    
    if len(indata) == 0:
        print("No audio input detected.")
        return
    
    audio_np = indata[:, 0].astype(np.float32)  # Normalize audio
    result = model.transcribe(audio_np, fp16=False, language="en", no_speech_threshold=0.3)

    # Print transcription
    if result['text']:
        print(result['text'], end='', flush=True)
    else:
        print("No speech detected in the current audio chunk.")

# Start the audio stream
try:
    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=audio_callback, blocksize=frames_per_buffer):
        print("Recording... Press Ctrl+C to stop.")
        sd.sleep(100000)  # Keep the stream open for a long duration
except KeyboardInterrupt:
    print("\nRecording stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sd.stop()  # Ensure the stream is stopped if interrupted
