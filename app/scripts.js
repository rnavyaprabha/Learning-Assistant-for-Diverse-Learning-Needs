// Global state and selectors
let isRecording = false; 
let transcription = '';
const transcriptionTextEl = document.getElementById("transcriptionText");
const summarizationTextEl = document.getElementById("summarizationText");
const translationTextEl = document.getElementById("translationText");
const startRecordingButton = document.getElementById("startRecordingButton");

// SpeechRecognition Setup
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.interimResults = true;
recognition.lang = 'en-US';
recognition.continuous = true;

function startTranscription() {
    recognition.start();
    startRecordingButton.innerText = "Stop Recording";
    startRecordingButton.style.backgroundColor = "#dc3545";
    isRecording = true;
}

function stopTranscription() {
    recognition.stop();
    startRecordingButton.innerText = "Start Recording";
    startRecordingButton.style.backgroundColor = "#28a745";
    isRecording = false;
}

// Handle Transcription Result
recognition.onresult = function(event) {
    transcription = Array.from(event.results)
        .map(result => result[0].transcript)
        .join('');
    transcriptionTextEl.innerText = transcription;
};

recognition.onstart = function() {
    console.log('Voice recognition started. Speak into the microphone.');
};

// Handle Errors
recognition.onerror = function(event) {
    console.error('Recognition Error:', event.error);
};

// Toggle recording on button click
startRecordingButton.onclick = function() {
    isRecording ? stopTranscription() : startTranscription();
};

// Switch Tabs
function showTab(tabId) {
    document.querySelectorAll('.result-container').forEach(tab => tab.style.display = 'none');
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).style.display = 'block';
    event.target.classList.add('active');
}

// Summarize and Translate Handlers
async function summarizeText() {
    if (!transcription.trim()) {
        summarizationTextEl.innerText = "No transcription available to summarize.";
        return;
    }
    summarizationTextEl.innerText = await fetchData('/summarize', transcription, summarizationTextEl);
}

async function translateText() {
    if (!transcription.trim()) {
        translationTextEl.innerText = "No transcription available to translate.";
        return;
    }
    translationTextEl.innerText = await fetchData('/translate', transcription, translationTextEl);
}

// Fetch data with loading indicator
async function fetchData(url, text, resultElement) {
    resultElement.innerText = url.includes('summarize') ? "Summarizing..." : "Translating...";
    resultElement.classList.add("loading");
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        resultElement.classList.remove("loading");
        return data.summary || data.translation || "No result available.";
    } catch (error) {
        resultElement.classList.remove("loading");
        console.error('Fetch Error:', error);
        return `Error: ${error.message}`;
    }
}

// Download text content
function downloadText(elementId, filename) {
    const text = document.getElementById(elementId).innerText;
    if (!text || text.includes("No transcription") || text.includes("No summary")) {
        alert("No content available for download.");
        return;
    }
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// Upload text file and display in transcription result
function uploadText() {
    const fileInput = document.getElementById('uploadTextFile');
    const file = fileInput.files[0];
    if (file && file.type === "text/plain") {
        const reader = new FileReader();
        reader.onload = function(event) {
            const text = event.target.result;
            transcription = text; // Update the global transcription variable
            document.getElementById("transcriptionText").innerText = text; // Display text in transcription area
        };
        reader.onerror = function() {
            alert("An error occurred while reading the file.");
        };
        reader.readAsText(file);
    } else {
        alert("Please upload a valid .txt file.");
    }
}


// Event Listeners for summarize, translate and switch tab
document.getElementById("summarizeButton").onclick = summarizeText;
document.getElementById("translateButton").onclick = translateText;
document.querySelectorAll('.tab').forEach(tab => tab.onclick = function() {
        showTab(this.getAttribute('onclick').split("'")[1]);
});