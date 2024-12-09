let socket = null;
let wsRecording = false;
let audioContext;
let analyserNode;
let microphone;
let processorNode;
const transcriptionTextEl = document.getElementById("transcriptionText");
const startRecordingButton = document.getElementById("startRecordingButton");

async function startWebSocket() {
    // Initialize WebSocket connection
    socket = new WebSocket("/ws/transcribe/");

    socket.onopen = async () => {
        transcriptionTextEl.innerText = "Listening...";
        startRecordingButton.innerText = "Stop Recording";
        startRecordingButton.style.backgroundColor = "#dc3545";
        wsRecording = true;

        // Access the user's microphone
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            console.log("Microphone access granted!");

            // Create an audio context to process the microphone input
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            microphone = audioContext.createMediaStreamSource(stream);

            // Create a ScriptProcessorNode to process audio chunks in real-time
            processorNode = audioContext.createScriptProcessor(4096, 1, 1); // Buffer size of 4096
            processorNode.onaudioprocess = (event) => {
                if (socket.readyState === WebSocket.OPEN) {
                    const float32Audio = event.inputBuffer.getChannelData(0); // Mono channel

                    // Convert Float32 audio to Int16
                    const int16Audio = new Int16Array(float32Audio.length);
                    for (let i = 0; i < float32Audio.length; i++) {
                        int16Audio[i] = Math.max(-1, Math.min(1, float32Audio[i])) * 0x7FFF; // Scale to Int16
                    }
                    console.log("Audio chunk (Int16):", int16Audio.slice(0, 10)); // Log the first 10 samples

                    // Send the converted audio buffer
                    socket.send(int16Audio.buffer);
                }
            };

            // Connect the microphone to the processor node
            microphone.connect(processorNode);
            processorNode.connect(audioContext.destination); // Optional: Remove this line if you don't need to hear the audio
        } catch (error) {
            console.error("Microphone access denied:", error);
        }
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
            console.error("Error:", data.error);
        } else if (data.is_final) {
            console.log("Final transcript:", data.transcript);
        } else {
            console.log("Partial transcript:", data.transcript);
        }
        transcriptionTextEl.innerText = data.transcript;
    };

    socket.onerror = (error) => console.error("WebSocket Error: ", error);
    socket.onclose = (event) => {
        console.log("WebSocket connection closed:", event);
        startRecordingButton.innerText = "Start Recording";
        startRecordingButton.style.backgroundColor = "#28a745";
        wsRecording = false;
    };
}


function stopWebSocket() {
    if (socket) {
        socket.close();
    }
    if (audioContext) {
        audioContext.close();  // Close the audio context
    }
}

export { startWebSocket, stopWebSocket, wsRecording, startRecordingButton };
