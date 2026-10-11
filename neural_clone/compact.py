from .llm import call_llm
from . import config

def compact_history(history):
    """
    Summarizes the old part of the history to save tokens.
    Keeps the system prompt and the most recent few messages.
    """
    if len(history) < 10:
        return history # Don't compact very short histories

    # Separate system prompt from conversation
    system_prompt = history[0] if history[0]["role"] == "system" else {"role": "system", "content": ""}
    conversation = history[1:] if history[0]["role"] == "system" else history

    # Keep the last 6 messages as they are
    keep_index = max(0, len(conversation) - 6)
    to_summarize = conversation[:keep_index]
    to_keep = conversation[keep_index:]

    # Create the summarization prompt
    summary_prompt = [
        {"role": "system", "content": "Summarize the following conversation history concisely. Retain all key technical decisions, file paths, and goals. Output the summary as a a list of bullet points."},
        {"role": "user", "content": f"Conversation to summarize:\n\n{str(to_summarize)}"}
    ]

    print("\n📉 History is too long. Compacting context...")
    summary_msg = call_llm(summary_prompt)
    summary_text = summary_msg.content if summary_msg.content else "No summary generated."

    # Create the new history: System Prompt + Summary + Recent Messages
    new_history = [
        system_prompt,
        {"role": "system", "content": f"Summary of previous conversation:\n{summary_text}"},
        *to_keep
    ]
    
    return new_history
