import os
from pathlib import Path
from .history import save_history, load_history

class Session:
    def __init__(self, session_id="default"):
        self.session_id = session_id
        self.history = load_history(session_id)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def add_raw_message(self, message_dict):
        self.history.append(message_dict)

    def save(self):
        save_history(self.session_id, self.history)

    def clear(self):
        self.history = []
        self.save()

def create_session(session_id="default"):
    return Session(session_id)
