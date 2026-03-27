from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import AnthropicChatModel
from agentscope.formatter import AnthropicMultiAgentFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command
from agentscope.pipeline import MsgHub
from agentscope.message import Msg
import os, asyncio
from dotenv import load_dotenv

load_dotenv()

toolkit = Toolkit()
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)

model = AnthropicChatModel(
    model_name="glm-4.6",
    api_key=os.environ["GLM_API_KEY"],
    stream=True,
    client_kwargs={"base_url": "https://api.z.ai/api/anthropic"},
)
formatter = AnthropicMultiAgentFormatter()

anton = ReActAgent(
    name="Anton",
    sys_prompt="Ты Антон — опытный геймдизайнер в игровой индустрии.",
    model=model,
    formatter=formatter,
    toolkit=Toolkit(),
    memory=InMemoryMemory(),
)

pavel = ReActAgent(
    name="Pavel",
    sys_prompt="Ты Павел — сеньор программист с большим опытом разработки игр.",
    model=model,
    formatter=formatter,
    toolkit=Toolkit(),
    memory=InMemoryMemory(),
)

yulia = ReActAgent(
    name="Yulia",
    sys_prompt="Ты Юлия — UX/UI дизайнер с опытом в игровой индустрии.",
    model=model,
    formatter=formatter,
    toolkit=Toolkit(),
    memory=InMemoryMemory(),
)


async def example_msghub() -> None:
    """Example of using MsgHub for multi-agent conversation."""
    async with MsgHub(
            [anton, pavel, yulia],
            announcement=Msg(
                "system",
                "Вы собрались вместе, чтобы сделать игру про ковбоев Westland. Представьтесь друг другу кратко. И озвучьте одну главную идею, которая, по вашему мнению, необходима в такой игре.",
                "system",
            ),
    ):
        await anton()
        await pavel()
        await yulia()


asyncio.run(example_msghub())


async def example_memory() -> None:
    """Print the memory of Anton."""
    print("Memory of Anton:")
    for msg in await anton.memory.get_memory():
        print(f"{msg.name}: {msg.get_text_content()}")


asyncio.run(example_memory())
