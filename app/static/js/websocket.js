let socket = null;
let wsRecording = false;
const transcriptionTextEl = document.getElementById("transcriptionText");
const startRecordingButton = document.getElementById("startRecordingButton");

function startWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8000/ws/transcribe");

    socket.onopen = () => transcriptionTextEl.innerText = "Listening...";
    socket.onmessage = (event) => transcriptionTextEl.innerText = JSON.parse(event.data).transcript;
    socket.onerror = (error) => console.error("WebSocket Error: ", error);
    socket.onclose = (event) => console.log("WebSocket connection closed:", event);

    startRecordingButton.innerText = "Stop Recording";
    startRecordingButton.style.backgroundColor = "#dc3545";
    wsRecording = true;
}

function stopWebSocket() {
    if (socket) {
        socket.close();
    }
    startRecordingButton.innerText = "Start Recording";
    startRecordingButton.style.backgroundColor = "#28a745";
    wsRecording = false;
}

export { startWebSocket, stopWebSocket, wsRecording, startRecordingButton };