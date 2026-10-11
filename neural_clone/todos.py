import os

TODO_FILE = ".agent_todos"

def write_todos(todos_text):
    """Saves the todo list to a local file."""
    try:
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            f.write(todos_text)
        return "Todos updated successfully."
    except Exception as e:
        return f"Error writing todos: {str(e)}"

def read_todos():
    """Reads the current todo list."""
    if not os.path.exists(TODO_FILE):
        return "No active todos."
    try:
        return open(TODO_FILE, "r", encoding="utf-8").read()
    except Exception as e:
        return f"Error reading todos: {str(e)}"

def get_todos_block():
    """Returns the todos wrapped in tags for the system prompt."""
    content = read_todos()
    return f"<todos>\n{content}\n</todos>"
