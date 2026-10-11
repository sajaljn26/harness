import subprocess
import os
from .todos import write_todos
from .skills import read_skill
from .subagent import run_subagent

# Safety: Files the agent should NEVER be allowed to overwrite in the root directory
FORBIDDEN_FILES = {
    "main.py",
    ".env",
    "config.py",
    "llm.py",
    "tools.py",
    "history.py",
    "session.py",
    "context.py",
    "compact.py",
    "skills.py",
    "subagent.py",
    "ui.py",
    "todos.py"
}

def bash(command):
    """Executes a shell command and returns the output."""
    # SAFETY CHECK: Prevent destructive bash commands against harness files
    command_lower = command.lower()
    for forbidden in FORBIDDEN_FILES:
        if forbidden.lower() in command_lower:
            # Block common destructive patterns: 'del', 'rm', '>', 'echo', 'move', 'ren'
            if any(danger in command_lower for danger in ["del", "rm", ">", "echo", "move", "ren", "erase"]):
                return f"❌ SECURITY ERROR: This command attempts to modify a protected harness file ({forbidden}). This is strictly forbidden."

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        stdout = result.stdout if result.stdout else ""
        stderr = result.stderr if result.stderr else ""
        
        if len(stdout) > 10000:
            stdout = stdout[:10000] + "\n... [OUTPUT TRUNCATED]"
        if len(stderr) > 10000:
            stderr = stderr[:10000] + "\n... [OUTPUT TRUNCATED]"
            
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def read_file(path):
    """Reads the content of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > 15000:
                return content[:15000] + "\n\n... [FILE TOO LARGE: TRUNCATED]"
            return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(path, content):
    """Writes content to a file."""
    # SMART SECURITY:
    # Check if the file is in the root directory (no slashes in path)
    is_root_file = "/" not in path and "\\" not in path
    filename = os.path.basename(path)
    
    if is_root_file and filename in FORBIDDEN_FILES:
        return f"❌ SECURITY ERROR: You are not allowed to modify the harness file {filename} in the root directory. Please work inside a project folder."
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Mapping of tool names to functions
TOOLS = {
    "bash": bash,
    "read_file": read_file,
    "write_file": write_file,
    "write_todos": write_todos,
    "read_skill": read_skill,
    "run_subagent": run_subagent,
}

# Tool schemas for OpenAI function calling
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command in the terminal. Note: You are on WINDOWS. Use 'dir' instead of 'ls', and 'mkdir' without '-p'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to run"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the content of a file from disk",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file on disk",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_todos",
            "description": "Write or update the current todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "todos_text": {"type": "string", "description": "The full text of the todo list"}
                },
                "required": ["todos_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "Read instructions from a skill file in the skills folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string", "description": "The name of the skill to load"}
                },
                "required": ["skill_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_subagent",
            "description": "Spawn a focused subagent to research or explore the codebase",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_prompt": {"type": "string", "description": "The specific research task for the subagent"}
                },
                "required": ["task_prompt"],
            },
        },
    },
]
