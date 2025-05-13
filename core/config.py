from dotenv import load_dotenv
import os
from rich.theme import Theme

# Load environment variables
load_dotenv()

# Initialize API clients
from openai import OpenAI
from elevenlabs.client import ElevenLabs

# Create API client instances
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Voice settings
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.0,
    "similarity_boost": 1.0,
    "style": 0.0,
    "use_speaker_boost": True
}

# Audio settings
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Default: Adam voice
DEFAULT_MODEL_ID = "eleven_turbo_v2_5"
DEFAULT_OUTPUT_FORMAT = "mp3_22050_32"

# Rich CLI theme
CLI_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "agent": "magenta",
    "user": "blue",
    "system": "dim",
    "recording": "yellow",
    "transcribing": "cyan",
    "thinking": "magenta",
    "speaking": "green"
}) 