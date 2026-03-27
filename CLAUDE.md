# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the project

```bash
python main.py
```

Requires a `.env` file in the project root with:
```
GLM_API_KEY=<your_key>
```

The script is interactive — it loops reading user input from stdin until the user types `exit`.

## Architecture

Single-file agent application built on [AgentScope](https://github.com/agentscope-ai/agentscope) (`agentscope` installed as editable from `D:\Projects\agentscope`).

**Flow:** `UserAgent` collects input → `ReActAgent` (named "Friday") processes it using the GLM model via an Anthropic-compatible API endpoint → loop repeats.

**Key components in `main.py`:**
- `AnthropicChatModel` — model client pointing to `https://api.z.ai/api/anthropic` with model `glm-4.6`
- `ReActAgent` — reasoning/acting agent with two registered tools: `execute_python_code` and `execute_shell_command`
- `AnthropicChatFormatter` — formats messages for the Anthropic API schema
- `InMemoryMemory` — conversation history, reset on each process start

## After any change to main.py

Run `python main.py` and verify it reaches `User Input:` without errors before committing.
