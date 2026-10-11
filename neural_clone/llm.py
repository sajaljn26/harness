from openai import OpenAI
from . import config
from .tools import TOOL_SCHEMAS
from .todos import get_todos_block # Import todo block helper

client = OpenAI(
    base_url=config.BASE_URL,
    api_key=config.API_KEY,
)

SYSTEM_PROMPT = """You are an expert coding agent. 
You have access to tools that allow you to interact with the file system and run commands.

For any task that takes more than one step, call write_todos first and plan it out. 
Send the whole list every time you call it - it replaces the old one.
Keep exactly one task in_progress, mark it done the moment it is finished, and move the next one to in_progress in the same call.

The current list is injected back to you every turn inside <todos> tags.

You have skills available. Each one is a set of instructions for a task.
If a skill matches what the user wants, call read_skill first and follow it.

If the user asks you to do something that requires checking files or running code, USE A TOOL. 
Do not just say you will do it; actually call the tool.
"""

def call_llm(messages):
    import re
    from .skills import skills_prompt
    todos = get_todos_block()
    skills = skills_prompt()
    
    if not messages or messages[0]["role"] != "system":
        messages.insert(0, {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{todos}\n\n{skills}"})
    else:
        # Update existing system prompt with new todos and skills
        content = messages[0]["content"]
        content = re.sub(r'<todos>.*?</todos>', '', content, flags=re.DOTALL)
        # we just append skills to the bottom for simplicity in this version
        messages[0]["content"] = f"{content}\n\n{todos}\n\n{skills}"

    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        tools=TOOL_SCHEMAS,
    )
    return response.choices[0].message
