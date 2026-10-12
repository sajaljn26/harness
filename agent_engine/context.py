def estimate_tokens(text):
    """
    A simple token estimator. 
    In a production app, you would use 'tiktoken' for OpenAI or a 
    specific tokenizer for Llama/Groq.
    For this harness, we assume 1 token ~= 4 characters.
    """
    return len(text) // 4

def get_history_tokens(history):
    """Calculates total tokens in the conversation history."""
    total = 0
    for msg in history:
        # Handle both dictionaries and Pydantic objects (ChatCompletionMessage)
        if isinstance(msg, dict):
            content = msg.get("content", "")
        else:
            content = getattr(msg, "content", "")
            
        if not content and hasattr(msg, "tool_calls"):
            content = str(msg.tool_calls)
        elif not content and isinstance(msg, dict) and "tool_calls" in msg:
            content = str(msg["tool_calls"])
            
        total += estimate_tokens(str(content))
    return total
