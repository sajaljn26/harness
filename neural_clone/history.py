import json
from pathlib import Path

def save_history(session_id, history):
    """Saves the conversation history to a JSON file."""
    session_dir = Path("sessions") / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    history_file = session_dir / "history.json"
    
    serializable_history = []
    for msg in history:
        if hasattr(msg, "model_dump"):
            # Use model_dump(exclude={"annotations"}) to remove non-serializable Groq/OpenAI fields
            try:
                data = msg.model_dump(exclude={"annotations"})
            except TypeError:
                data = msg.model_dump()
            serializable_history.append(data)
        elif isinstance(msg, dict):
            # Also remove annotations if they exist in the dict
            cleaned_msg = {k: v for k, v in msg.items() if k != "annotations"}
            serializable_history.append(cleaned_msg)
        else:
            serializable_history.append({"role": "system", "content": str(msg)})
            
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(serializable_history, f, indent=2)



def load_history(session_id):
    """Loads the conversation history from a JSON file."""
    history_file = Path("sessions") / session_id / "history.json"
    if not history_file.exists():
        return []
    
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
        return []
