import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, StreamingResponse

from agentscope.agent import ReActAgent
from agentscope.formatter import AnthropicMultiAgentFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import AnthropicChatModel
from agentscope.pipeline import MsgHub
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command

load_dotenv()

_API_KEY = os.environ.get("GLM_API_KEY")
if not _API_KEY:
    raise RuntimeError("GLM_API_KEY environment variable is not set")

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def index():
    return FileResponse("index.html")


def _make_agent(cfg: dict) -> ReActAgent:
    tk = Toolkit()
    tk.register_tool_function(execute_python_code)
    tk.register_tool_function(execute_shell_command)

    model = AnthropicChatModel(
        model_name="glm-4.6",
        api_key=_API_KEY,
        stream=True,
        client_kwargs={"base_url": "https://api.z.ai/api/anthropic"},
    )
    agent = ReActAgent(
        name=cfg["name"],
        sys_prompt=cfg["prompt"],
        model=model,
        formatter=AnthropicMultiAgentFormatter(),
        toolkit=tk,
        memory=InMemoryMemory(),
    )
    agent.set_console_output_enabled(False)
    return agent


def _event(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


async def _run(agents_cfg: list, system_text: str):
    agents = [_make_agent(cfg) for cfg in agents_cfg]
    try:
        async with MsgHub(
            agents,
            announcement=Msg("system", system_text, "system"),
        ):
            for agent in agents:
                yield _event({"type": "agent_typing", "name": agent.name})
                msg = await agent()
                yield _event({
                    "type": "agent_message",
                    "name": msg.name,
                    "text": msg.get_text_content() or "",
                })
    except Exception as exc:
        yield _event({"type": "error", "message": str(exc)})
        return

    yield _event({"type": "conversation_done"})


@app.post("/run")
async def run(request: Request):
    data = await request.json()
    agents_cfg = data.get("agents", [])
    system_text = data.get("system", "")

    if not (1 <= len(agents_cfg) <= 10):
        async def err():
            yield _event({"type": "error", "message": "Нужно от 1 до 10 агентов"})
        return StreamingResponse(err(), media_type="text/event-stream")

    return StreamingResponse(
        _run(agents_cfg, system_text),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
