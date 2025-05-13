import asyncio
from core.agent import VoiceAgent
from core.config import CLI_THEME
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
import time

# Initialize rich console with our theme
console = Console(theme=CLI_THEME)

async def run_voice_agent():
    """
    Start the main loop for the voice agent.

    This continuously:
    - Records the user's voice input
    - Transcribes it to text
    - Sends the text to the LangGraph agent
    - Speaks back the result
    Press Ctrl+C to exit the loop.
    """
    agent = VoiceAgent()

    # Welcome message
    console.print(Panel.fit(
        "[agent]🎙️ Voice Agent[/agent] is ready! Press [warning]Ctrl+C[/warning] to exit.",
        title="Welcome",
        border_style="agent"
    ))
    console.print(f"[system]Thread ID:[/system] {agent.thread_id}")

    while True:
        try:
            # Recording status
            with Live(
                Spinner("dots", text="[recording]Recording your instruction...[/recording] Press Enter to stop."),
                console=console,
                refresh_per_second=10,
                transient=True
            ) as live:
                user_message = agent.audio_processor.record_audio()

            # Show transcribed text
            console.print("\n[user]You said:[/user]")
            console.print(Panel(
                user_message.content,
                border_style="user"
            ))

            # Processing status
            with Live(
                Spinner("dots", text="[thinking]Processing your request...[/thinking]"),
                console=console,
                refresh_per_second=10,
                transient=True
            ) as live:
                response = await agent.process_user_input(user_message)

            # Show agent's response
            console.print("\n[agent]Agent:[/agent]")
            console.print(Panel(
                response,
                border_style="agent"
            ))

            # Speaking status
            with Live(
                Spinner("dots", text="[speaking]Speaking response...[/speaking]"),
                console=console,
                refresh_per_second=10,
                transient=True
            ) as live:
                agent.audio_processor.speak_response(response)

            # Add a small pause between interactions
            time.sleep(0.5)
            console.print()

        except KeyboardInterrupt:
            console.print("\n[warning]Goodbye![/warning]")
            break

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            console.print(f"\n[error]{error_message}[/error]")
            agent.audio_processor.speak_response(error_message)

if __name__ == "__main__":
    try:
        asyncio.run(run_voice_agent())
    except KeyboardInterrupt:
        console.print("\n[warning]Exiting...[/warning]") 