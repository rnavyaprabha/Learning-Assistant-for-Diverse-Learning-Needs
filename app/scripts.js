let isRecording = false; // Track the recording state
let transcription = ''; // Store the transcription text

// Initialize SpeechRecognition for transcription
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.interimResults = true; // Get interim results for live feedback
recognition.lang = 'en-US'; // Set the language
recognition.continuous = true; // Enable continuous speech recognition

recognition.onresult = function(event) {
    const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');

    transcription = transcript; // Store the transcription
    document.getElementById("transcriptionText").innerText = transcript; // Display the transcription
};

recognition.onstart = function() {
    console.log('Voice recognition started. Speak into the microphone.');
};

recognition.onerror = function(event) {
    console.error('Error occurred in recognition: ' + event.error);
};

// Toggle recording on button click
document.getElementById("startRecordingButton").onclick = function() {
    if (isRecording) {
        recognition.stop();
        this.innerText = "Start Recording";
        this.style.backgroundColor = "#28a745"; // Green for start
        this.style.color = "white";
        isRecording = false;
    } else {
        transcription = ''; // Clear previous transcription
        recognition.start();
        this.innerText = "Stop Recording";
        this.style.backgroundColor = "#dc3545"; // Red for stop
        this.style.color = "white";
        isRecording = true;
    }
};

// Show Tab function to switch between tabs without triggering actions
function showTab(tabId) {
    document.querySelectorAll('.result-container').forEach(tab => {
        tab.style.display = 'none';
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabId).style.display = 'block';
    event.target.classList.add('active');
}

// Summarize Text on button click
document.getElementById("summarizeButton").onclick = async function() {
    if (!transcription.trim()) {
        document.getElementById("summarizationText").innerText = "No transcription available to summarize.";
        return;
    }
    const data = await fetchData('/summarize', transcription, "Summarizing...");
    document.getElementById("summarizationText").innerText = data.summary || "No summary available.";
};

// Translate Text on button click
document.getElementById("translateButton").onclick = async function() {
    if (!transcription.trim()) {
        document.getElementById("translationText").innerText = "No transcription available to translate.";
        return;
    }
    const data = await fetchData('/translate', transcription, "Translating...");
    document.getElementById("translationText").innerText = data.translation || "No translation available.";
};

// Fetch data with loading indicator
async function fetchData(url, text, loadingMessage) {
    const resultId = url.includes('summarize') ? "summarizationText" : url.includes('translate') ? "translationText" : "transcriptionText";
    const resultElement = document.getElementById(resultId);
    resultElement.classList.add("loading");
    resultElement.innerText = loadingMessage;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        resultElement.classList.remove("loading");
        return data;
    } catch (error) {
        resultElement.innerText = "Error: " + error.message;
        resultElement.classList.remove("loading");
        throw error;
    }
}

// Attach click events to the tab elements to call showTab without triggering actions
document.querySelectorAll('.tab').forEach(tab => {
    tab.onclick = function() {
        showTab(this.getAttribute('onclick').split("'")[1]);
    };
});