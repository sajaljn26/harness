import json
import os
from neural_clone.llm import call_llm
from neural_clone.tools import TOOLS
from neural_clone.session import Session
from neural_clone.context import get_history_tokens
from neural_clone.compact import compact_history
from neural_clone import config
from neural_clone.ui import ui

def main():
    ui.banner()
    
    session_name = "default"
    session = Session(session_name)
    history = session.history

    while True:
        user_input = input("\n> ").strip()
        if not user_input:
            continue
            
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # --- SLASH COMMANDS ---
        if user_input.startswith("/"):
            parts = user_input.split(" ", 1)
            cmd = parts[0].lower()
            
            if cmd == "/clear":
                session.clear()
                if os.path.exists(".agent_todos"):
                    os.remove(".agent_todos")
                history = []
                ui.agent("🧠 Memory wiped. Todo list cleared. I'm ready for a fresh start!")
                continue
                
            elif cmd == "/session":
                if len(parts) < 2:
                    ui.agent("Please provide a session name: `/session my_project`")
                    continue
                
                session_name = parts[1]
                session = Session(session_name)
                history = session.history
                ui.agent(f"📂 Switched to session: {session_name}")
                continue
            
            else:
                ui.agent(f"Unknown command: {cmd}. Try `/clear` or `/session [name]`")
                continue
        # ----------------------

        ui.user(user_input)
        history.append({"role": "user", "content": user_input})
        
        # --- CONTEXT COMPACTION CHECK ---
        current_tokens = get_history_tokens(history)
        if current_tokens > config.CONTEXT_WINDOW * config.COMPACT_AT:
            with ui.working("Compacting memory..."):
                history = compact_history(history)
                session.history = history
        # --------------------------------
        
        while True:
            with ui.working("Thinking..."):
                try:
                    message = call_llm(history)
                except Exception as e:
                    error_msg = f"API Error: {str(e)}"
                    ui.agent(f"⚠️ {error_msg}")
                    history.append({"role": "assistant", "content": error_msg})
                    break
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    fn_name = tool_call.function.name
                    
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        error_feedback = f"JSON Parse Error in tool {fn_name}. Please retry with valid JSON arguments."
                        ui.agent(f"⚠️ {error_feedback}")
                        history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": fn_name,
                            "content": error_feedback
                        })
                        continue
                    
                    ui.tool(fn_name, args, "Executing...")
                    
                    result = TOOLS[fn_name](**args)
                    
                    ui.tool(fn_name, args, result)
                    
                    history.append(message)
                    history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": fn_name,
                        "content": result,
                    })
                continue 
            
            if message.content:
                ui.agent(message.content)
                history.append({"role": "assistant", "content": message.content})
            
            break 
        
        session.save()

if __name__ == "__main__":
    main()
