# Autonomous AI Coding Harness

A modular software orchestration layer developed in Python to enable Large Language Models (LLMs) to autonomously interact with a local development environment. This system bridges the gap between a stateless LLM and a stateful operating system, allowing for automated code generation, execution, and project management.

## 🏗️ System Architecture

The harness follows a decoupled, modular architecture to ensure separation of concerns:

```text
[ User ] <---> [ main.py (Orchestrator) ]
                        |
        --------------------------------------------
        |               |               |          |
  [ llm.py ]      [ tools.py ]    [ session.py ] [ context.py ]
 (Brain/API)     (Hands/OS)      (Memory/JSON)  (Optimization)
        |               |               |          |
    [ Groq ]      [ Local OS ]    [ history.json ] [ Summary ]
```

## ✨ Key Features

### Tool-Use & Agency
- **Bash Execution**: A wrapper for system shell commands to facilitate environment navigation and script execution.
- **File System Access**: Read and write files directly to the disk to create and modify codebases.
- **Subagent Research**: Spawn specialized "mini-agents" to perform deep-dive research on specific parts of a codebase.
- **Custom Skills**: A plugin-like system that loads technical instructions from markdown files.

### Memory & Context
- **Persistent Sessions**: Conversation histories are serialized to JSON, allowing the agent to resume tasks across restarts.
- **Context Compaction**: Automatically summarizes the preceding conversation when token thresholds are reached to preserve essential state.

### Security Framework
- **Root Directory Protection**: A strict exclusion list prevents the agent from modifying its own source code.
- **Bash Filtering**: Shell commands are scanned for forbidden patterns involving root-level files before execution.

## 🛠️ Testing & Validation

To ensure the reliability and safety of the harness, a dedicated test suite has been implemented. These tests validate the core engine's stability without requiring expensive API calls.

### Test Suite Coverage
- **Security Firewall**: Validates that the agent cannot modify protected harness files (e.g., `main.py`, `.env`) via `write_file` or `bash` commands.
- **Context Compaction**: Verifies that the history is correctly condensed when token thresholds are exceeded, maintaining the system prompt while reducing noise.
- **Session Persistence**: Ensures that conversation state is correctly serialized and deserialized from JSON.

### Running the Tests
The test suite can be executed using the built-in Python `unittest` framework:
```bash
python tests.py
```

## 🚀 Setup & Usage

### Prerequisites
- Python 3.10+
- An API key from a provider supporting the OpenAI API specification (e.g., Groq).

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install required dependencies:
   ```bash
   pip install openai rich
   ```
3. Configure environment variables in a `.env` file:
   ```text
   API_KEY=your_api_key
   BASE_URL=https://api.groq.com/openai/v1
   MODEL=llama-3.1-70b-versatile
   ```

### Execution
```bash
python main.py
```

## ⚠️ Limitations & Future Work

As an MVP (Minimum Viable Product), the current version has the following limitations and planned upgrades:

- **Sandboxing**: Currently runs on the local host OS. Future versions will implement **Docker Containerization** to isolate the agent from the host system entirely.
- **Token Accuracy**: Uses a character-based estimation for tokens. Moving to `tiktoken` will provide exact token counts.
- **State Storage**: Uses JSON files for persistence. Future iterations will implement a **Vector Database (RAG)** for handling massive codebases.
- **Error Recovery**: Currently relies on basic retry loops. Implementing a **Reflection-based Critic** would allow the agent to self-correct more complex bugs.

## 🎓 Engineering Learning Outcomes
The development of this harness provided deep experience in:
- **Agentic Workflow Design**: Implementing the "Plan-Act-Observe" loop.
- **State Serialization**: Managing complex object types for persistent storage.
- **Context Engineering**: Balancing detail and token constraints through automated summarization.
- **Safety Engineering**: Implementing guardrails to prevent autonomous agents from performing destructive operations.
