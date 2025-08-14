Voicer - The latest product of Minerva AI
A robust, voice-controlled file management agent that lets you manage your local file system using natural language commands. This project is built using a custom stack of best-in-class free API tiers, including OpenRouter for intelligence, Hugging Face for transcription, and ElevenLabs for voice output.

Features
Natural Language Voice Commands: Speak naturally to your computer to manage files.

Intelligent Agent Brain: Uses OpenRouter to access powerful language models (e.g., Claude 3 Haiku) to understand complex commands.

Free Tier Speech-to-Text: Leverages the Hugging Face Inference API for fast and free audio transcription.

Realistic Voice Feedback: Uses ElevenLabs for high-quality, natural-sounding voice responses.

Comprehensive File Operations:

Create and write to files (write_file)

Read the contents of files (read_file)

List files and folders in a directory (list_directory)

Delete files (delete_file)

Create new directories (create_directory)

The Final Working Architecture
This project went through significant debugging. The final, stable architecture is as follows:

Voice Input: Audio is captured from a specific microphone device on your machine using sounddevice.

Transcription (Ears): The raw audio is sent to the Hugging Face Inference API to be transcribed into text by a Whisper model.

Agent Brain: The transcribed text is sent to a ReAct Agent powered by OpenRouter, which decides which action to take.

File Tools (Hands): The agent selects a custom, robust Python tool (write_file, read_file, etc.) to execute the desired file system operation.

Text Response: The result of the action (e.g., "File created successfully") is generated.

Voice Output (Voice): The text response is sent to the ElevenLabs API to be converted into speech and played back.

Getting Started
Prerequisites
Python 3.9+

Git

An internet connection

1. Installation
First, clone the repository and navigate into the project directory.

```bash
git clone https://github.com/ankitdutta428/Voicer.git
cd voicer
```

Next, create a requirements.txt file in the main project folder and paste the following dependencies into it:

requirements.txt

```
text
langchain
langchain-openai
langchain-community
openai
python-dotenv
sounddevice
numpy
scipy
requests
rich
elevenlabs
```
Now, install all the required libraries using pip:

```bash
pip install -r requirements.txt
```
2. Set Up API Keys
This project requires three separate API keys. Create a file named .env in the root of your project folder.

```bash
# For Windows
copy con .env
# For macOS/Linux
touch .env
```
Now, edit the .env file and add your keys like this.

.env

text
```
# For the LLM "Brain" - https://openrouter.ai/
OPENROUTER_API_KEY="your_openrouter_key_starting_with_sk-or"

# For Text-to-Speech "Voice" - https://elevenlabs.io/
ELEVEN_API_KEY="your_elevenlabs_api_key"

# For Speech-to-Text "Ears" - https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY="your_hugging_face_token_starting_with_hf_"
```

3. Configure Your Microphone (Crucial Step!)
The application needs to know exactly which microphone to listen to. To avoid errors, we must find your microphone's specific ID.

A. Find Your Microphone ID:
Create a temporary Python file named check_mic.py and paste this code into it:

```python
# check_mic.py
import sounddevice as sd
print("Searching for audio devices...")
print(sd.query_devices())
```
Run this script from your terminal:

```bash
python check_mic.py
```
Look through the output list for your primary microphone. You will see a number at the start of the line, like > 1 Microphone (Realtek(R) Audio), MME. The number 1 is your device ID.

B. Update the Configuration:
Open the core/config.py file and change the MICROPHONE_DEVICE_ID to the number you just found.

```python
# core/config.py

# ... other code ...

# --- Audio Settings ---
# Change this number to match your device ID from the check_mic.py script
MICROPHONE_DEVICE_ID = 1 
# ... rest of the code ...
```
Usage
You are now ready to run the agent!

Start the agent from your terminal:

```bash
python main.py
```
Wait for the welcome message. When you see "Start speaking...", say your command clearly.

Press the Enter key when you are finished speaking.

The agent will show its thought process in the terminal, execute the command, and speak the result back to you.

To exit the agent, press Ctrl+C in the terminal.

Example Commands
"Make me a file with name ideas.txt and write down 'Build a voice agent'."

"Show me all the files in this directory."

"What are the contents of requirements.txt?"

"Create a new folder called archive."

"Delete the file ideas.txt."

How It Works: The ReAct Agent Loop
A common point of confusion is seeing JSON in the logs. This is not your input; it is the AI agent's internal thought process.

Thought: The AI brain receives your English command (e.g., "Create a file called test.txt") and thinks about what to do.

Action: It decides which tool to use (write_file) and creates a structured, machine-readable JSON instruction for that tool. This is what you see in the logs (Action Input: {"file_path": "test.txt", ...}).

Observation: The tool runs with the JSON instruction and returns a result (e.g., "Successfully wrote to test.txt").

Thought: The AI brain observes this result and decides if the task is complete or if another step is needed. If complete, it generates the final spoken response.

Troubleshooting
Microphone Not Recording / Script Hangs: This is almost always a permissions issue or an incorrect device ID.

Ensure you have set the correct MICROPHONE_DEVICE_ID in core/config.py.

Check your OS settings (Windows Privacy > Microphone or macOS System Settings > Privacy & Security > Microphone) to ensure your terminal/Python has permission to access the microphone.

401 Unauthorized Error: This means an API key is wrong.

If the error happens during transcription, check your HUGGINGFACE_API_KEY.

If the error happens after transcription ("Processing your request..."), check your OPENROUTER_API_KEY.

If the error happens during voice output, check your ELEVEN_API_KEY.

503 Service Unavailable or 504 Gateway Timeout from Hugging Face: This can happen with the free API tier if the model is under heavy load or needs to "wake up." Simply wait a minute and try your command again.

PydanticUserError or other LangChain errors: The Python ecosystem moves fast. This usually indicates a library version mismatch. Ensure your installed packages match the requirements.txt file.

Contributing
Contributions are welcome! If you've improved the tools or added new functionality, please feel free to submit a Pull Request.