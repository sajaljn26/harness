import unittest
import os
from agent_engine.tools import bash, write_file
from agent_engine.compact import compact_history

class TestHarness(unittest.TestCase):
    
    def test_security_firewall_write(self):
        """Ensure the agent cannot overwrite forbidden files using write_file."""
        result = write_file("main.py", "print('hacked')")
        self.assertIn("SECURITY ERROR", result)
        
    def test_security_firewall_bash(self):
        """Ensure the agent cannot overwrite forbidden files using bash commands."""
        # Test 'del' command
        result = bash("del main.py")
        self.assertIn("SECURITY ERROR", result)
        
        # Test 'echo' redirection
        result = bash("echo 'hacked' > main.py")
        self.assertIn("SECURITY ERROR", result)

    def test_context_compaction(self):
        """Verify that history is condensed when it grows too large."""
        # Create a fake history with 20 messages
        history = [{"role": "system", "content": "You are a helper."}]
        for i in range(20):
            history.append({"role": "user", "content": f"Message {i}"})
            history.append({"role": "assistant", "content": f"Response {i}"})
            
        compacted = compact_history(history)
        
        # The result should be significantly shorter than the original
        self.assertTrue(len(compacted) < len(history))
        # It should still start with the system prompt
        self.assertEqual(compacted[0]["role"], "system")

if __name__ == "__main__":
    unittest.main()
