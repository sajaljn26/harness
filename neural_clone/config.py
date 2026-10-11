import os
from pathlib import Path

# We check if a .env file exists and load it manually for simplicity, 
# though in production you'd use 'python-dotenv'.
ENV_FILE = Path(".env")
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

# Groq/OpenAI compatible settings
# For Groq: https://api.groq.com/openai/v1
BASE_URL = os.environ.get("BASE_URL", "https://api.groq.com/openai/v1")
API_KEY = os.environ.get("API_KEY", "")
MODEL = os.environ.get("MODEL", "llama-3.1-70b-versatile")

# How much room the model has, and how we spend it.
CONTEXT_WINDOW = int(os.environ.get("CONTEXT_WINDOW", 128_000))
COMPACT_AT = 0.85  # compact once the prompt crosses this much of the window
COMPACT_TO = 0.35  # and cut back to this much, so it does not retrigger soon

if not API_KEY:
    print("WARNING: API_KEY not found in environment or .env file!")
