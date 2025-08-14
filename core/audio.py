# core/audio.py

import os
import io
import threading
import requests
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from langchain_core.messages import HumanMessage
from rich.console import Console
from elevenlabs import play

# Import the necessary settings and clients from our updated config
from .config import (
    elevenlabs_client,
    huggingface_api_key,
    HF_TRANSCRIPTION_URL,
    MICROPHONE_DEVICE_ID,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_VOICE_ID,
    DEFAULT_MODEL_ID,
    CLI_THEME
)

console = Console(theme=CLI_THEME)

class AudioProcessor:
    """
    Handles all voice input and output.
    - Records audio from a specific microphone.
    - Transcribes audio using the Hugging Face API.
    - Speaks text responses using the ElevenLabs API.
    """
    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        self.sample_rate = sample_rate
        self._recording = False
        self._frames = []

    def _record_thread(self):
        """A separate thread to capture audio from the specified microphone."""
        try:
            # Use the specific microphone device ID and sample rate from config
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16', device=MICROPHONE_DEVICE_ID) as stream:
                while self._recording:
                    audio_chunk, _ = stream.read(1024)
                    self._frames.append(audio_chunk)
        except Exception as e:
            console.print(f"[error]Microphone recording error: {e}[/error]")
            self._recording = False

    def record_audio(self) -> HumanMessage:
        """Records audio and transcribes it using the Hugging Face API."""
        self._frames = []
        self._recording = True
        
        console.print("[recording]Start speaking... Press Enter when you're done.[/recording]")
        
        thread = threading.Thread(target=self._record_thread)
        thread.start()
        
        input() # Wait for the user to press Enter
        self._recording = False
        thread.join()

        if not self._frames:
            console.print("[warning]No audio was recorded.[/warning]")
            return HumanMessage(content="")

        console.print("[transcribing]Recording stopped. Transcribing with Hugging Face...[/transcribing]")
        
        # --- START OF HUGGING FACE TRANSCRIPTION LOGIC ---
        try:
            audio_array = np.concatenate(self._frames, axis=0)
            audio_bytes = io.BytesIO()
            write(audio_bytes, self.sample_rate, audio_array)
            audio_bytes.seek(0)

            headers = {
               "Authorization": f"Bearer {huggingface_api_key}",
               "Content-Type": "audio/wav"
            }
            
            response = requests.post(HF_TRANSCRIPTION_URL, headers=headers, data=audio_bytes.read(), timeout=45)

            if response.status_code != 200:
                console.print(f"[error]Hugging Face API Error {response.status_code}: {response.text}[/error]")
                return HumanMessage(content="")

            result = response.json()
            transcribed_text = result.get('text', '').strip()

            if transcribed_text:
                console.print(f"[user_input]You said: {transcribed_text}[/user_input]")
                return HumanMessage(content=transcribed_text)
            else:
                console.print("[warning]Audio was recorded but transcription was empty.[/warning]")
                return HumanMessage(content="")

        except Exception as e:
            console.print(f"[error]An error occurred during transcription: {e}[/error]")
            return HumanMessage(content="")
        # --- END OF HUGGING FACE TRANSCRIPTION LOGIC ---

    def speak_response(self, text: str):
        """Uses the working ElevenLabs client to speak the response."""
        cleaned_text = text.replace("**", "")
        console.print(f"[agent_response]Agent: {cleaned_text}[/agent_response]")
        try:
            audio_stream = elevenlabs_client.text_to_speech.convert(
                voice_id=DEFAULT_VOICE_ID,
                model_id=DEFAULT_MODEL_ID,
                text=cleaned_text
            )
            if audio_stream:
                play(audio_stream)
        except Exception as e:
            console.print(f"[error]Failed to play audio from ElevenLabs: {e}[/error]")

