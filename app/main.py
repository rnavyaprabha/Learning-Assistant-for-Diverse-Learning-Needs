# main.py
from fastapi import FastAPI, File, WebSocket, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import numpy as np
import whisper 
#from .WhisperSTT import transcribe_audio
#from translator import translate_text
from .Summarization import summarize_notes
from .Summarization import summarize_text
import io

app = FastAPI()

# Load environment variables
load_dotenv()

# Set the path for the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

# Serve the current directory as static
app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")

# Load the Whisper model
model = whisper.load_model("tiny")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse(html_file_path)

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

# Endpoint for Audio-to-Text
@app.post("/transcribe/")
async def audio_to_text():#file: UploadFile = File(...)):
    #audio_data = await file.read()  # Read audio file from request
    #transcription = transcribe_audio(io.BytesIO(audio_data))
    # Transcription data from a local file
    with open("app/notes.txt", "r") as file:
        notes_content = file.read()
    transcription=notes_content
    return {"transcription": transcription}

# Endpoint for Translation
@app.post("/translate/")
async def translate():#text: str, target_language: str = "es"):
    ##translated_text = translate_text(text, target_language)
    translated_text = 'Deep Learninges un subconjunto de la inteligencia artificial y el aprendizaje automático que aprovecha las redes neuronales para aprender de datos no estructurados, como imágenes, audio y texto. Utiliza estructuras de múltiples capas para comprender patrones y relaciones complejos dentro de los datos. Los avances clave incluyen redes neuronales convolucionales para el reconocimiento de imágenes y redes neuronales recurrentes para datos secuenciales. La retropropagación, las funciones de activación y las técnicas de regularización son fundamentales para el aprendizaje profundo. Los desafíos incluyen la necesidad de grandes conjuntos de datos, demandas computacionales y problemas de interpretabilidad. El aprendizaje profundo encuentra aplicaciones en la atención médica, el procesamiento del lenguaje natural, los sistemas autónomos, las finanzas y el entretenimiento. El futuro del aprendizaje profundo implica modelos livianos para dispositivos de borde, mejor interpretabilidad y aprendizaje multimodal para obtener información más completa.'
    translated_text = ''
    return {"translation": translated_text}

@app.post("/summarize_notes/")
async def summarize_notes():
    summary = summarize_notes()
    return {"summary": summary}


# Define a Pydantic model for the input text
class SummarizeRequest(BaseModel):
    text: str

# Endpoint for Summarization
@app.post("/summarize/")
async def summarize(request: SummarizeRequest):
    summary = summarize_text(request.text)  # Use the text from the request
    return {"summary": summary}