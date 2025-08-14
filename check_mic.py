# check_mic.py
import sounddevice as sd
from rich.console import Console

console = Console()

console.print("[bold yellow]--- Checking for Audio Devices ---[/bold yellow]")
console.print("This script will list all audio devices found by the 'sounddevice' library.")

try:
    # Query for all devices
    devices = sd.query_devices()
    
    if not devices:
        console.print("\n[bold red]❌ No audio devices found at all.[/bold red]")
        console.print("Please ensure your microphone is properly connected.")
    else:
        console.print("\n[bold green]✅ Found the following audio devices:[/bold green]")
        console.print(devices)
        
        # Specifically check for a default input device
        try:
            default_input_device = sd.query_devices(kind='input')
            if default_input_device:
                 console.print("\n[bold green]✅ SUCCESS: A default microphone was found.[/bold green]")
            else:
                 console.print("\n[bold red]❌ ERROR: No default microphone was found.[/bold red]")
                 console.print("Your system has audio devices, but none is set as the default input.")
                 console.print("Please check your Windows Sound settings and set a default microphone.")

        except Exception as e:
            console.print(f"\n[bold red]Could not query for default input device: {e}[/bold red]")

except Exception as e:
    console.print(f"\n[bold red]An error occurred while querying for devices: {e}[/bold red]")
    console.print("This can indicate a problem with your system's audio drivers.")
