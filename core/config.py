# core/config.py

import os
from dotenv import load_dotenv
from rich.theme import Theme
from elevenlabs.client import ElevenLabs

# Load all environment variables from .env file
load_dotenv()

# --- API Keys ---
# Note: The OpenRouter key will be used directly in agent.py
eleven_api_key = os.getenv("ELEVEN_API_KEY")
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

# --- Client Initialization ---
# Initialize the ElevenLabs client for text-to-speech
if not eleven_api_key:
    raise ValueError("ELEVEN_API_KEY not found in .env file.")
elevenlabs_client = ElevenLabs(api_key=eleven_api_key)

# --- Transcription Settings ---
# The working Hugging Face model URL from our successful test
if not huggingface_api_key:
    raise ValueError("HUGGINGFACE_API_KEY not found in .env file.")
HF_TRANSCRIPTION_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"

# --- Audio Settings ---
# Device ID for your microphone (found with our test script)
MICROPHONE_DEVICE_ID = 1 
# Sample rate must be 16000 Hz for Whisper models
DEFAULT_SAMPLE_RATE = 16000 
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB" # Default: Adam voice
DEFAULT_MODEL_ID = "eleven_turbo_v2_5"

# --- Rich CLI Theme ---
CLI_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "agent_response": "cyan",
    "user_input": "bold blue",
    "system": "dim",
    "recording": "yellow",
    "transcribing": "cyan",
    "thinking": "magenta",
    "speaking": "green"
})
