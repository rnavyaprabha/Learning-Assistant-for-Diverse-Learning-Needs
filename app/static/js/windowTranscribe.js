const transcriptionTextEl = document.getElementById("transcriptionText");
// SpeechRecognition Setup
let isRecording = false; // Global state
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.interimResults = true;
recognition.lang = 'en-US';
recognition.continuous = true;

function startTranscription() {
    recognition.start();
    startRecordingButton.innerText = "Stop Recording";
    startRecordingButton.style.backgroundColor = "#dc3545";
    transcriptLabel.innerText = "Transcription Result:";
    transcriptionTextEl.innerText = "Listening...";
    isRecording = true;
}

function stopTranscription() {
    recognition.stop();
    startRecordingButton.innerText = "Start Recording";
    startRecordingButton.style.backgroundColor = "#28a745";
    isRecording = false;
    if (transcriptionTextEl.innerText === "Listening...") {
        transcriptionTextEl.innerText = "No transcription available.";
    }
}

// Handle Transcription Result
recognition.onresult = function(event) {
    transcriptionTextEl.innerText = 
        Array.from(event.results)
            .map(result => result[0].transcript)
            .join('');
};

recognition.onstart = function() {
    console.log('Voice recognition started. Speak into the microphone.');
};

// Handle Errors
recognition.onerror = function(event) {
    console.error('Recognition Error:', event.error);
};

export { startTranscription, stopTranscription, isRecording};