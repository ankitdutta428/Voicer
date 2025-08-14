# core/tools.py

import os
import json # Import the JSON library
from langchain.tools import BaseTool
from typing import Type, Dict

# --- THIS IS THE FINAL FIX ---
# Each tool's `_run` method will now check if the input is a string.
# If it is, it will parse it from a JSON string into a Python dictionary.
# This makes our tools robust against the AgentExecutor's bug.

class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = "Use this tool to write specified content to a file. The input must be a single JSON object with 'file_path' and 'content' keys."

    def _run(self, tool_input: str | Dict):
        """Writes content to a file, safely handling string or dictionary input."""
        try:
            # Check if the input is a string and parse it if necessary
            if isinstance(tool_input, str):
                data = json.loads(tool_input)
            else:
                data = tool_input

            # Manual validation inside the tool
            if 'file_path' not in data or 'content' not in data:
                return "Error: Your instruction was missing 'file_path' or 'content'."
            
            file_path = data['file_path']
            content = data['content']
            
            full_path = os.path.expanduser(file_path)
            parent_dir = os.path.dirname(full_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except json.JSONDecodeError:
            return "Error: The input was not valid JSON."
        except Exception as e:
            return f"Error during file write operation: {e}"

class ReadFileTool(BaseTool):
    name: str = "read_file"
    description: str = "Use this tool to read the content of a file at a specified path."

    def _run(self, tool_input: str | Dict):
        try:
            if isinstance(tool_input, str):
                data = json.loads(tool_input)
            else:
                data = tool_input

            if 'file_path' not in data:
                return "Error: Your instruction was missing 'file_path'."
            
            file_path = data['file_path']
            full_path = os.path.expanduser(file_path)
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found at {data.get('file_path')}"
        except Exception as e:
            return f"Error reading from file: {e}"

# Apply the same robust pattern to all other tools...

class ListDirectoryTool(BaseTool):
    name: str = "list_directory"
    description: str = "Use this to list the contents of a specified directory."

    def _run(self, tool_input: str | Dict):
        try:
            if isinstance(tool_input, str):
                data = json.loads(tool_input)
            else:
                data = tool_input

            path = data.get('path', '.')
            full_path = os.path.expanduser(path)
            return "\n".join(os.listdir(full_path)) or f"The directory '{path}' is empty."
        except FileNotFoundError:
            return "Error: Directory not found."
        except Exception as e:
            return f"Error listing directory: {e}"

class DeleteFileTool(BaseTool):
    name: str = "delete_file"
    description: str = "Use this tool to delete a file at a specified path."

    def _run(self, tool_input: str | Dict):
        try:
            if isinstance(tool_input, str):
                data = json.loads(tool_input)
            else:
                data = tool_input

            if 'file_path' not in data:
                return "Error: Your instruction was missing 'file_path'."

            file_path = data['file_path']
            full_path = os.path.expanduser(file_path)
            os.remove(full_path)
            return f"Successfully deleted file: {file_path}"
        except FileNotFoundError:
            return f"Error: File not found at {data.get('file_path')}"
        except Exception as e:
            return f"Error deleting file: {e}"

class CreateDirectoryTool(BaseTool):
    name: str = "create_directory"
    description: str = "Use this tool to create a new directory at a specified path."

    def _run(self, tool_input: str | Dict):
        try:
            if isinstance(tool_input, str):
                data = json.loads(tool_input)
            else:
                data = tool_input

            if 'path' not in data:
                return "Error: Your instruction was missing 'path'."

            path = data['path']
            full_path = os.path.expanduser(path)
            os.makedirs(full_path, exist_ok=True)
            return f"Successfully created directory: {path}"
        except Exception as e:
            return f"Error creating directory: {e}"
