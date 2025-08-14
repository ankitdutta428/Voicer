# test_recording.py (Final Version with Hugging Face API)
import os
import io
import requests
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from dotenv import load_dotenv
from rich.console import Console

console = Console()

# --- Configuration ---
# The microphone device ID we found earlier
MICROPHONE_DEVICE_ID = 1 
# The sample rate needs to match what the model expects
SAMPLE_RATE = 16000 
# The working Hugging Face model URL from our successful test
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"

def run_full_recording_test():
    """
    Tests recording from a specific microphone and transcribing it using
    the working Hugging Face Inference API.
    """
    console.print(f"[bold yellow]--- Full Test: Recording from Mic #{MICROPHONE_DEVICE_ID} & Transcribing with Hugging Face ---[/bold yellow]")
    
    try:
        # --- Step 1: Load Hugging Face API Key ---
        load_dotenv()
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            raise ValueError("ERROR: HUGGINGFACE_API_KEY not found in .env file.")
        
        console.print("✅ Hugging Face API key loaded.")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "audio/wav"
        }

        # --- Step 2: Record Audio from Microphone ---
        audio_data = []

        def record_callback(indata, frames, time, status):
            if status:
                console.print(f"[red]Recording Status Warning: {status}[/red]")
            audio_data.append(indata.copy())

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', 
                            device=MICROPHONE_DEVICE_ID, callback=record_callback):
            console.print("[bold green]Start speaking... Press Enter to stop recording.[/bold green]")
            input()  # Wait for user to press Enter

        console.print("[dim]Recording stopped. Preparing audio data...[/dim]")

        if not audio_data:
            console.print("\n[bold red]❌ RECORDING FAILED.[/bold red]", "No audio data was captured.")
            return

        audio_array = np.concatenate(audio_data, axis=0)
        audio_bytes = io.BytesIO()
        write(audio_bytes, SAMPLE_RATE, audio_array)
        audio_bytes.seek(0)

        # --- Step 3: Transcribe Audio with Hugging Face ---
        console.print(f"[dim]Sending audio to Hugging Face model: {API_URL}...[/dim]")
        response = requests.post(API_URL, headers=headers, data=audio_bytes.read(), timeout=45)

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        result = response.json()
        transcribed_text = result.get('text', '').strip()

        if transcribed_text:
            console.print("\n[bold green]✅✅✅ FULL TEST PASSED! ✅✅✅[/bold green]")
            console.print(f"Successfully transcribed your voice: \"{transcribed_text}\"")
        else:
            console.print("\n[bold red]❌ TRANSCRIPTION FAILED.[/bold red]")
            console.print("Audio was recorded but the API returned empty text.")

    except Exception as e:
        console.print(f"\n[bold red]An error occurred during the test: {e}[/bold red]")

if __name__ == "__main__":
    run_full_recording_test()
