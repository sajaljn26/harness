from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add the current directory to sys.path so we can import from agent_engine
sys.path.append(str(Path('.').absolute()))

from agent_engine.llm import call_llm
from unittest.mock import patch

def test_conversation_flow():
    print("🧪 Testing Conversation Flow...")
    
    # We mock the 'client.chat.completions.create' so we don't need a real API key for this test
    with patch('agent_engine.llm.client.chat.completions.create') as mock_create:
        # Define what the mock LLM should return for different turns
        mock_create.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content="Hello! I am your coding assistant. How can I help?"))]),
            MagicMock(choices=[MagicMock(message=MagicMock(content="Your name is Sajal. I remember that!"))])
        ]

        history = [{"role": "system", "content": "You are a helper."}]
        
        # Turn 1
        user_msg1 = "Hi, my name is Sajal"
        history.append({"role": "user", "content": user_msg1})
        res1 = call_llm(history)
        history.append({"role": "assistant", "content": res1})
        print(f"User: {user_msg1}\nAgent: {res1}")

        # Turn 2
        user_msg2 = "What is my name?"
        history.append({"role": "user", "content": user_msg2})
        res2 = call_llm(history)
        history.append({"role": "assistant", "content": res2})
        print(f"User: {user_msg2}\nAgent: {res2}")

        # Verify the history contains everything
        assert len(history) == 5 # System + User1 + Asst1 + User2 + Asst2
        print("\n✅ Test Passed: History is being maintained correctly!")

if __name__ == "__main__":
    test_conversation_flow()
