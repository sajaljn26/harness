# Autonomous AI Engineering Framework

A high-performance, modular orchestration layer developed in Python to enable Large Language Models (LLMs) to transition from passive chat interfaces to autonomous software engineers. This system implements a "Plan-Act-Observe" loop, allowing an AI to navigate local file systems, execute shell commands, and manage long-term project state.

## 🏛️ Engineering Philosophy

Most AI interfaces are stateless wrappers. This project is designed as a **stateful agentic framework**. Instead of relying on a single prompt, the system implements a recursive loop:
1. **Perceive**: Analyze the current state of the directory and conversation history.
2. **Plan**: Utilize a persistent `Todo` system to break complex goals into atomic tasks.
3. **Act**: Execute specific tool calls (Bash, File I/O, Subagents).
4. **Observe**: Read the tool output and reflect on whether the task was successful.
5. **Correct**: If a tool fails or a bug is found, the agent modifies its plan and retries.

## ⚙️ System Architecture

The framework is built on a decoupled, modular architecture to ensure scalability and ease of maintenance:

### Core Modules
- **`agent_engine/llm.py`**: The communication bridge. Manages the system prompt and handles the conversion of LLM outputs into executable function calls.
- **`agent_engine/tools.py`**: The interface to the OS. Provides a secure wrapper around shell commands and file system operations.
- **`agent_engine/session.py` & `history.py`**: The persistence layer. Uses JSON serialization to maintain conversation state and project memory across application restarts.
- **`agent_engine/context.py` & `compact.py`**: The optimization layer. Implements a sliding-window context management system that summarizes old history to maximize the LLM's token efficiency.
- **`agent_engine/ui.py`**: The presentation layer. Uses the `rich` library to provide a high-fidelity, real-time view of the agent's internal thought process.

### Advanced Features
- **Hierarchical Agency**: Ability to spawn specialized **Subagents** to perform isolated research tasks without polluting the primary agent's context.
- **Skill Plugin System**: A dynamic loading mechanism that reads `.md` files from a skills directory, allowing the agent to acquire new technical expertise without code changes.
- **Security Firewall**: A multi-layered protection system that prevents the agent from modifying the harness source code or executing destructive commands on the host OS.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- API key from an OpenAI-compatible provider (e.g., Groq).

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
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

## 🛠️ Developer's Guide: Adding New Tools

The engine is designed for extensibility. To add a new tool:
1. Define a Python function in `agent_engine/tools.py`.
2. Add the function to the `TOOLS` dictionary.
3. Define the tool's parameters in the `TOOL_SCHEMAS` list using the OpenAI function-calling specification.

## 🛡️ Security & Validation

The system includes a comprehensive `tests.py` suite to validate:
- **Firewall Integrity**: Ensuring forbidden files cannot be modified.
- **Memory Stability**: Verifying that context compaction preserves essential state.
- **Session Logic**: Ensuring history is correctly serialized and restored.

Run tests via:
```bash
python tests.py
```

## 🎓 Learning Outcomes
This project served as an exploration of:
- **Autonomous Agent Loops**: Moving beyond request-response patterns.
- **State Persistence**: Managing complex object serialization for long-term memory.
- **Context Engineering**: Designing a system to handle LLM token limits via automated summarization.
- **Security Engineering**: Building guardrails for autonomous code execution.
