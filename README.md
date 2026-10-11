# 🚀 Sajal's AI Coder

A professional-grade, autonomous coding agent harness built in Python. This project transforms a Large Language Model (LLM) from a simple chatbot into an active software engineer capable of planning, executing, and managing full-scale coding tasks on a local machine.

## 🌟 Overview

Sajal's AI Coder is an orchestration layer that connects an LLM (via Groq/OpenAI API) to a local runtime environment. Unlike basic AI wrappers, this harness implements an **Agentic Loop**, allowing the AI to use a set of tools to interact with the OS, maintain long-term memory across sessions, and manage complex tasks through internal planning.

## ✨ Key Features

### 🛠️ Tool-Use & Agency
The agent can perform real-world actions through a set of integrated tools:
- **Bash Execution**: Run terminal commands to navigate directories, install packages, or execute scripts.
- **File System Access**: Read and write files directly to the disk to create and modify codebases.
- **Subagent Research**: Spawn specialized "mini-agents" to perform deep-dive research on specific parts of a codebase without polluting the main context.
- **Custom Skills**: A plugin-like system where the agent can load `.md` or `.txt` files from a skills directory to learn new technical domains on the fly.

### 🧠 Advanced Memory & Context
- **Persistent Sessions**: Conversation history is serialized to JSON, allowing the agent to remember project goals and secrets across restarts.
- **Autonomous Planning**: Implements a `Todo` system. For multi-step tasks, the agent creates a checklist and tracks its own progress (`pending` $\rightarrow$ `in_progress` $\rightarrow$ `done`).
- **Context Compaction**: To prevent "token overflow," the harness automatically summarizes old parts of the conversation while retaining critical technical decisions.

### 🛡️ Security & Robustness
- **Root Directory Protection**: A built-in security firewall prevents the agent from modifying or deleting the harness's own source code or sensitive files like `.env`.
- **Robust JSON Parsing**: Includes a failure-recovery loop that catches LLM formatting errors and asks the AI to self-correct.
- **Output Truncation**: Prevents "context explosion" by truncating massive tool outputs.

### 🎨 Professional UI
- Built with the `rich` library to provide a high-fidelity terminal experience featuring:
  - **Markdown Rendering**: Code and documentation are displayed beautifully.
  - **Interactive Panels**: Tool calls and results are shown in distinct, colored panels.
  - **Thinking Spinners**: Visual feedback while the LLM is processing.

## 🏗️ Architecture

The project follows a modular design:
- `llm.py`: Handles the communication with the LLM and manages the system prompt.
- `tools.py`: Defines the "Hands" of the agent and the security guardrails.
- `session.py` & `history.py`: Manages the persistence of chat logs.
- `context.py` & `compact.py`: Handles token tracking and memory compression.
- `ui.py`: The presentation layer for the terminal.
- `main.py`: The central orchestrator and agent loop.

## 🚀 Setup & Usage

### Prerequisites
- Python 3.10+
- A Groq API Key (or any OpenAI-compatible API key)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```
2. Install dependencies:
   ```bash
   pip install openai rich
   ```
3. Create a `.env` file in the root directory:
   ```text
   API_KEY=your_groq_api_key
   BASE_URL=https://api.groq.com/openai/v1
   MODEL=llama-3.1-70b-versatile
   ```

### Running the Agent
```bash
python main.py
```

**Useful Commands:**
- `/clear`: Wipe current memory and todos.
- `/session [name]`: Switch to a different project context.
- `quit`: Exit the program.

## 🎓 Learning Outcomes
Building this project provided deep experience in:
- **Asynchronous-style Agentic Loops** and tool-calling protocols.
- **State Management** and JSON serialization for persistent AI memory.
- **Security Engineering** for LLMs to prevent accidental file system destruction.
- **Token Optimization** through algorithmic summarization.
