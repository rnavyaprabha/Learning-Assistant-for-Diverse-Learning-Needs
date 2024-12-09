from fastapi import FastAPI, File, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import os
from services.Translation import translate_text
from services.Transcription import transcribe_audio
#from services.Transcription_test import transcribe_audio
from services.Summarization import summarize_text
from services.Correction import correct_grammar

app = FastAPI()

# Middleware for handling headers and trusted hosts
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Load environment variables
load_dotenv()

# Path to the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

# Serve static files
static_dir = os.path.dirname(__file__)+"/static/"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Root endpoint to serve the HTML file
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse(html_file_path)

# Define Pydantic models for request validation
class TranslateRequest(BaseModel):
    text: str
    target_language: str

class SummarizeRequest(BaseModel):
    text: str

# Endpoint for translation
@app.post("/translate/")
async def translate(request: TranslateRequest):
    translated_text = translate_text(request.text, request.target_language)
    return {"translation": translated_text}

# Endpoint for summarization
@app.post("/summarize/")
async def summarize(request: SummarizeRequest):
    summary = summarize_text(request.text)
    return {"summary": summary}

# Endpoint for grammar correction
@app.post("/correction/")
async def correction(request: SummarizeRequest):
    corrected_text = correct_grammar(request.text)
    return {"corrected_text": corrected_text}

# WebSocket endpoint for audio transcription
@app.websocket("/ws/transcribe/")
async def transcribe_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected.")
    try:
        async for transcription in transcribe_audio(websocket):
            print("transcription", transcription)
            if transcription.get("error"):
                # Handle error in transcription
                await websocket.send_json({"error": transcription["error"]})
            else:
                # Send transcription result back to client
                await websocket.send_json(transcription)
    except Exception as e:
        print(f"Error in WebSocket handler: {e}")
        await websocket.send_json({"error": str(e)})
    finally:
        print("WebSocket connection closing.")
        await websocket.close()