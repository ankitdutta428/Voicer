from langchain_community.tools.file_management import (
    CopyFileTool,       # Copy a file from one path to another
    DeleteFileTool,     # Delete a file
    FileSearchTool,     # Search for files by name or pattern
    ListDirectoryTool,  # List contents of a folder
    MoveFileTool,       # Move a file to a different location
    ReadFileTool,       # Read the contents of a file
    WriteFileTool       # Write or update a file
)

def get_file_tools():
    """
    Initialize and return a list of file management tools.
    
    Returns:
        list: A list of initialized file management tools
    """
    return [
        CopyFileTool(),
        DeleteFileTool(),
        FileSearchTool(),
        ListDirectoryTool(),
        MoveFileTool(),
        ReadFileTool(),
        WriteFileTool(),
    ] 