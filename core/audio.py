from dotenv import load_dotenv
import os

load_dotenv()

# Initialize API clients
from openai import OpenAI
from elevenlabs.client import ElevenLabs

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Required imports for audio processing
import io
import threading
from typing import List
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import signal

# Voice output and message handling
from elevenlabs import play, VoiceSettings
from langchain_core.messages import HumanMessage

# Import configuration
from .config import (
    openai_client,
    elevenlabs_client,
    DEFAULT_VOICE_SETTINGS,
    DEFAULT_SAMPLE_RATE,
    DEFAULT_VOICE_ID,
    DEFAULT_MODEL_ID,
    DEFAULT_OUTPUT_FORMAT,
    CLI_THEME
)

# Initialize rich console
from rich.console import Console
console = Console(theme=CLI_THEME)

class AudioProcessor:
    """
    Handles all voice input and output functionality for the voice agent.

    This class supports:
    - Recording audio from the user's microphone
    - Transcribing the recorded audio into text using OpenAI's gpt-4o-mini-transcribe
    - Converting agent text responses into audio using ElevenLabs and playing them

    Attributes:
        sample_rate (int): Audio sample rate in Hz (default is 16000)
        _recording (bool): Flag to control the recording state
        voice_settings (VoiceSettings): Configuration for ElevenLabs voice synthesis
    """

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        """
        Initialize the AudioProcessor with default voice settings.

        Args:
            sample_rate (int): Sample rate for recording audio (Hz)
        """
        self.sample_rate = sample_rate
        self._recording = False
        self.voice_settings = VoiceSettings(**DEFAULT_VOICE_SETTINGS)
        self._stop_event = threading.Event()

    def record_audio(self) -> HumanMessage:
        """
        Records audio from the user's microphone until Enter is pressed,
        then sends the audio to OpenAI for transcription.

        Returns:
            HumanMessage: The transcribed user input as a LangChain message
        """
        audio_data: List[np.ndarray] = []
        self._recording = True
        self._stop_event.clear()

        def record_callback():
            """Capture live audio chunks from the microphone while recording is active."""
            try:
                with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as stream:
                    while self._recording and not self._stop_event.is_set():
                        audio_chunk, _ = stream.read(1024)
                        audio_data.append(audio_chunk)
            except Exception as e:
                console.print(f"[error]Error during recording: {str(e)}[/error]")
                self._recording = False

        def stop_recording():
            """Wait for Enter key to stop recording."""
            try:
                input()
                self._recording = False
            except (KeyboardInterrupt, EOFError):
                self._recording = False
                self._stop_event.set()

        # Start recording and wait for user input in parallel threads
        recording_thread = threading.Thread(target=record_callback)
        stop_thread = threading.Thread(target=stop_recording)
        
        recording_thread.start()
        stop_thread.start()
        
        try:
            stop_thread.join()
            recording_thread.join()
        except KeyboardInterrupt:
            self._recording = False
            self._stop_event.set()
            recording_thread.join()
            raise

        if not audio_data:
            raise KeyboardInterrupt("Recording was interrupted")

        # Merge and prepare the audio buffer for transcription
        audio_array = np.concatenate(audio_data, axis=0)
        audio_bytes = io.BytesIO()
        write(audio_bytes, self.sample_rate, audio_array)
        audio_bytes.seek(0)
        audio_bytes.name = "audio.wav"

        # Transcribe the audio using OpenAI
        transcription = openai_client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_bytes
        )

        return HumanMessage(content=transcription.text)

    def speak_response(self, text: str):
        """
        Converts a given text response into speech using ElevenLabs and plays it.

        Args:
            text (str): The message to convert and speak
        """
        cleaned_text = text.replace("**", "")  # Remove markdown formatting
        audio = elevenlabs_client.text_to_speech.convert(
            voice_id=DEFAULT_VOICE_ID,
            output_format=DEFAULT_OUTPUT_FORMAT,
            text=cleaned_text,
            model_id=DEFAULT_MODEL_ID,
            voice_settings=self.voice_settings
        )
        play(audio)