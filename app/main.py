# main.py
from fastapi import FastAPI, File, WebSocket, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
import os
from dotenv import load_dotenv
import numpy as np
import whisper 
#from .WhisperSTT import transcribe_audio
#from translator import translate_text
#from .summarization import summarize_notes
import io

app = FastAPI()

# Load environment variables
load_dotenv()
print("Current Working Directory:", os.getcwd())
print("API Key in main.py:", os.getenv("OPENAI_API_KEY"))  # Check if it loads correctly

# Set the path for the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

# Load the Whisper model
model = whisper.load_model("tiny")

# Set up a WebSocket route for real-time transcription
@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive audio data from the client
            audio_data = await websocket.receive_bytes()

            # Process and transcribe audio data
            transcription = model.transcribe(np.frombuffer(audio_data, dtype=np.float32), fp16=False)

            # Send the transcription back to the client
            await websocket.send_text(transcription['text'])

        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break

    await websocket.close()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse(html_file_path)

# Endpoint for Audio-to-Text
@app.post("/transcribe/")
async def audio_to_text():#file: UploadFile = File(...)):
    #audio_data = await file.read()  # Read audio file from request
    #transcription = transcribe_audio(io.BytesIO(audio_data))
    transcription = "My name is Martin and I am a software developer. Today we are going to learn how to use FastAPI."
    return {"transcription": transcription}

# Endpoint for Translation
@app.post("/translate/")
async def translate():#text: str, target_language: str = "es"):
    ##translated_text = translate_text(text, target_language)
    translated_text = 'Mi nombre es Martin y soy un desarrollador de software. El dia de hoy vamos a aprender a usar FastAPI.'
    return {"translation": translated_text}

# Endpoint for Summarization
@app.post("/summarize/")
async def summarize():#text: str):
    #summary = summarize_notes()
    summary = 'We are going to learn hot to use FastAPI.'
    return {"summary": summary}