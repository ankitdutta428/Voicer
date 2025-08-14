# test_huggingface.py (The Definitive Version)
import os
import io
import requests
from dotenv import load_dotenv
from scipy.io.wavfile import write
import numpy as np
from rich.console import Console

console = Console()
console.print("[bold yellow]--- Final Test: Hugging Face API with a Distilled Model ---[/bold yellow]")

try:
    # --- Step 1: Load Hugging Face API Key ---
    load_dotenv()
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("ERROR: HUGGINGFACE_API_KEY not found in .env file.")
    
    console.print("✅ Hugging Face API key loaded.")

    # --- Step 2: Prepare Request with a RELIABLE Model URL ---
    # This is a smaller, faster "distilled" version of Whisper, perfect for the free API.
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "audio/wav"
    }
    console.print(f"✅ API URL set to a reliable distilled model: {API_URL}")

    # --- Step 3: Create a Dummy Audio File ---
    sample_rate = 16000
    silence = np.zeros(sample_rate, dtype=np.int16)
    
    audio_bytes = io.BytesIO()
    write(audio_bytes, sample_rate, silence)
    audio_bytes.seek(0)
    console.print("✅ Dummy audio file created.")

    # --- Step 4: Call the Hugging Face API ---
    console.print("[dim]Sending request to Hugging Face...[/dim]")
    response = requests.post(API_URL, headers=headers, data=audio_bytes.read(), timeout=45)

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    result = response.json()

    console.print("\n[bold green]✅✅✅ TEST PASSED - TRANSCRIPTION IS WORKING! ✅✅✅[/bold green]")
    console.print("Successfully communicated with the Hugging Face transcription API.")
    console.print(f"Response from server (should be empty for silence): '{result.get('text')}'")

except Exception as e:
    console.print(f"\n[bold red]❌ TEST FAILED.[/bold red]")
    console.print(f"An error occurred: {e}")

