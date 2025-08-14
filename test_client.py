import os 
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

load_dotenv()


# Initialize the client with the API key
client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))
# Use the specific ID for the voice you want. "Rachel" is a common choice.
# You can find more in the ElevenLabs Voice Library.
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" 
MODEL_ID = "eleven_multilingual_v2" # A stable, high-quality model

try:
    print("Generating audio with the correct method and parameters...")

    # --- FINAL CORRECTION ---
    # The method is `convert`, and the parameters are `voice_id` and `model_id`.
    audio_stream = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id=MODEL_ID,
        text="This is the final test. It should now work without any errors."
    )
    # --- END OF CORRECTION ---

    print("Audio generated successfully!")

    # The `save` function is the best way to write the audio stream to a file.
    # It handles the stream iterator correctly.
    save(audio_stream, "test_output.mp3")
    print("Audio saved to test_output.mp3")

    # To play the audio, you must either read it from the file or generate it again,
    # because the initial stream is "consumed" when you save it.
    # For a simple confirmation, we can play it from the saved file.
    
    print("Playing audio from the saved file...")
    with open("test_output.mp3", "rb") as f:
        audio_for_playback = f.read()
    
    play(audio_for_playback)
    print("Playback finished.")

except Exception as e:
    print(f"An error occurred: {e}")

