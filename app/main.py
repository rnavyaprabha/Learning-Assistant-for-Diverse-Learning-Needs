# main.py
from fastapi import FastAPI, File, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import numpy as np
from dotenv import load_dotenv
from .services.Translation import translate_text
from .services.Transcription import transcribe_audio
from .services.Summarization import summarize_text

app = FastAPI()

# Load environment variables
load_dotenv()

# Set the path for the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

# Serve the current directory as static
app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)+"/static/"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse(html_file_path)

# Endpoint for Audio-to-Text transcription
@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await transcribe_audio(websocket)
    except WebSocketDisconnect:
        print("WebSocket connection closed")

# Define a Pydantic model for the input text
class TranslateRequest(BaseModel):
    text: str
    target_language: str

# Endpoint for Translation
@app.post("/translate/")
async def translate(request: TranslateRequest):
    translated_text = translate_text(request.text, request.target_language)
    return {"translation": translated_text}

# Define a Pydantic model for the input text
class SummarizeRequest(BaseModel):
    text: str

# Endpoint for Summarization
@app.post("/summarize/")
async def summarize(request: SummarizeRequest):
    summary = summarize_text(request.text)  # Use the text from the request
    return {"summary": summary}