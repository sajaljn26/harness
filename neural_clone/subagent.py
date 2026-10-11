import os

def run_subagent(task_prompt):
    """
    Spawns a focused subagent to perform a specific read-only task.
    The subagent has a different system prompt to ensure it stays on task.
    """
    # HIGHLY STRICT system prompt to prevent the subagent from attempting tool calls
    # or "thinking out loud" which can break the API response.
    SUBAGENT_PROMPT = f"""You are a focused research subagent. 
Your ONLY goal is to provide a concise, plain-text answer to the user's request.

STRICT RULES:
1. DO NOT attempt to call tools.
2. DO NOT use thought blocks or <thought> tags.
3. DO NOT explain your process.
4. PROVIDE ONLY the final answer/report.
5. If you cannot find the answer, simply say 'Information not found'.

Current directory: {os.getcwd()}
"""
    
    from .llm import call_llm
    
    messages = [
        {"role": "system", "content": SUBAGENT_PROMPT},
        {"role": "user", "content": task_prompt}
    ]
    
    try:
        # We call the LLM without passing tools to the subagent, 
        # ensuring it can ONLY return text.
        from .llm import client, config
        from openai import OpenAI
        
        # We use a direct client call here to ensure NO tools are passed
        response = client.chat.completions.create(
            model=config.MODEL,
            messages=messages,
            tools=None # Explicitly disable tools for the subagent
        )
        
        return response.choices[0].message.content if response.choices[0].message.content else "Subagent returned no result."
    except Exception as e:
        return f"Subagent error: {str(e)}"
