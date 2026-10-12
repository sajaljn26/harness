# Autonomous AI Coding Harness

A modular software orchestration layer developed in Python to enable Large Language Models (LLMs) to autonomously interact with a local development environment. This system bridges the gap between a stateless LLM and a stateful operating system, allowing for automated code generation, execution, and project management.

## Technical Overview

The harness implements an agentic loop that allows an LLM to transition from a passive chat interface to an active agent. By utilizing tool-calling protocols, the system enables the model to perform file system operations and execute shell commands, while maintaining a persistent state across multiple sessions.

## System Architecture

The project is structured into specialized modules to ensure separation of concerns and maintainability:

### 1. LLM Integration (`llm.py`)
Handles the communication with OpenAI-compatible APIs (e.g., Groq, OpenAI). It manages the system prompt and the conversion of LLM responses into executable tool calls.

### 2. Toolset & Agency (`tools.py`)
Provides the agent with a set of "hands" to interact with the OS:
- **Bash Execution**: A wrapper for system shell commands to facilitate environment navigation and script execution.
- **File I/O**: Functions for reading and writing files to the local disk.
- **Planning (Todos)**: A state-tracking mechanism that allows the agent to define and track multi-step task lists.
- **Knowledge Retrieval (Skills)**: A plugin system that loads specific technical instructions from markdown files to augment the agent's domain expertise.

### 3. Memory & Session Management (`session.py`, `history.py`)
Implements long-term persistence:
- **Session Isolation**: Allows for multiple independent project contexts.
- **JSON Serialization**: Conversation histories are serialized to disk, enabling the agent to resume complex tasks across application restarts.

### 4. Context Optimization (`context.py`, `compact.py`)
To manage the finite context window of LLMs, the harness implements a compaction layer:
- **Token Estimation**: Tracks the approximate token count of the current prompt.
- **Contextual Summarization**: When a threshold is reached, the system automatically summarizes the preceding conversation and replaces bulky history with a concise technical summary to preserve essential state.

### 5. Security Framework
To prevent accidental or malicious system modification, the harness implements a security firewall:
- **Protected File List**: A strict exclusion list prevents the agent from modifying its own source code or environment configuration.
- **Bash Filtering**: Shell commands are scanned for forbidden patterns involving root-level files before execution.

## Installation and Configuration

### Prerequisites
- Python 3.10+
- An API key from a provider supporting the OpenAI API specification (e.g., Groq).

### Setup
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

## Command Reference

- `/clear`: Wipes the current conversation history and clears the active todo list.
- `/session [name]`: Switches the active context to a specific session ID.
- `quit`: Terminates the application.

## Engineering Learning Outcomes
The development of this harness provided deep insights into:
- **Agentic Workflow Design**: Implementing the "Plan-Act-Observe" loop.
- **State Serialization**: Managing complex object types for persistent storage.
- **Context Engineering**: Balancing detail and token constraints through automated summarization.
- **Safety Engineering**: Implementing guardrails to prevent autonomous agents from performing destructive operations on the host OS.
