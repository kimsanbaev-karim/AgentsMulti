# AgentsMulti

A sandbox for multi-agent conversation on [AgentScope](https://github.com/modelscope/agentscope):
three `ReActAgent` instances with different professional roles share one `MsgHub` and talk to
each other about a task, instead of a single assistant answering alone.

The agents are a game designer, a senior gameplay programmer and a UX/UI designer. Given an
announcement — "you are here to make a cowboy game, introduce yourselves and name the one idea
this game needs" — each speaks in turn, sees what the others said, and keeps its own
`InMemoryMemory` across the exchange.

Each agent carries a `Toolkit` with `execute_python_code` and `execute_shell_command`, so a
reply can be backed by actually running something rather than by describing it.

## Two ways to run it

`main.py` runs the scripted exchange in the terminal and then prints one agent's memory, which
makes it easy to see what each participant actually retained.

`server.py` exposes the same setup over FastAPI with a streaming endpoint and serves
`index.html`, a single-page UI where the conversation appears message by message.

## Running

```bash
pip install -r requirements.txt
python main.py          # terminal exchange
python server.py        # web UI
```

Or with Docker:

```bash
docker compose up
```

Both paths need a `.env` file in the project root:

```
GLM_API_KEY=<your key>
```

The model is GLM-4.6, reached through an Anthropic-compatible endpoint at `api.z.ai`, so the
Anthropic client and formatter from AgentScope work against it unchanged. Swapping in another
Anthropic-compatible provider is a matter of changing `base_url` and `model_name`.
