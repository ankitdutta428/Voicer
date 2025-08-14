import asyncio
import uuid  # <-- ADDED IMPORT
from rich.console import Console
from rich.panel import Panel

# Correctly import ReactAgent
from core.agent import ReactAgent
from core.audio import AudioProcessor

# Set up the console (assuming a theme might be in your config)
try:
    from core.config import CLI_THEME
    console = Console(theme=CLI_THEME)
except (ImportError, KeyError):
    console = Console()


async def run_voice_agent():
    """
    The main asynchronous loop for the voice agent.
    """
    # 1. Initialize the agent and audio processor
    agent = ReactAgent()
    audio_processor = AudioProcessor()

    # 2. Create a unique thread ID for this conversation session
    thread_id = str(uuid.uuid4())
    
    # 3. Print the welcome message with the session ID
    welcome_message = "🎙️ Voice Agent is ready! Press Ctrl+C to exit."
    console.print(Panel(welcome_message, title="Welcome", subtitle=f"Session ID: {thread_id}"))

    try:
        while True:
            try:
                # Record and transcribe user input
                user_message = audio_processor.record_audio()

                if not user_message.content or "try again" in user_message.content.lower():
                    console.print("[warning]Skipping empty or unclear audio.[/warning]")
                    continue
                
                console.print("[thinking]Processing your request...[/thinking]")
                
                # 4. Pass the thread_id to the agent with each call
                agent_response = agent.get_agent_response(user_message, thread_id=thread_id)
                
                # Speak the agent's response
                audio_processor.speak_response(agent_response.content)

            except KeyboardInterrupt:
                # This allows gracefully exiting the loop with Ctrl+C
                console.print("\n[bold cyan]Voice agent shutting down.[/bold cyan]")
                break
            except Exception as e:
                console.print(f"[error]An unexpected error occurred: {e}[/error]")
                continue

    except KeyboardInterrupt:
        # This handles a Ctrl+C pressed outside the recording input
        console.print("\n[bold cyan]Voice agent shut down by user.[/bold cyan]")

if __name__ == "__main__":
    try:
        asyncio.run(run_voice_agent())
    except KeyboardInterrupt:
        pass
