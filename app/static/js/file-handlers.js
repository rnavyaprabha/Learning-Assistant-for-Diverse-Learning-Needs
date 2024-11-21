
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
            document.getElementById("transcriptionText").innerText = text;
        };
        reader.onerror = function() {
            alert("An error occurred while reading the file.");
        };
        reader.readAsText(file);
    } else {
        alert("Please upload a valid .txt file.");
    }
}
export { downloadText, uploadText };