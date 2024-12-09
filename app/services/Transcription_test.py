async def test_audio_generator(websocket):
    # Async generator to yield audio chunks
    try:
        print("Audio generator started...")
        while True:
            audio_chunk = await websocket.receive_bytes()  # Wait for raw audio data
            print(f"Received audio chunk of size {len(audio_chunk)} bytes")
            if len(audio_chunk) > 0:
                print(f"Sending audio chunk: {audio_chunk[:10]}...")  # Print the first 10 bytes
                yield audio_chunk  # Yield raw audio for testing
            else:
                print("Received empty audio chunk!")
    except Exception as e:
        print(f"Audio generator stopped: {e}")

async def transcribe_audio(websocket):
    print("Starting audio generator test...")

    # Directly test the audio generator without streaming recognition
    async for audio_chunk in test_audio_generator(websocket):
        print(f"Test chunk received: {audio_chunk[:10]}...")  # Print first 10 bytes for inspection
        yield {
            "transcript": str(audio_chunk[:10]),
            "is_final": True,
        }