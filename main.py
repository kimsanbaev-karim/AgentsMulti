from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import AnthropicChatModel
from agentscope.formatter import AnthropicChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command
import os, asyncio
from dotenv import load_dotenv
load_dotenv()


async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    agent = ReActAgent(
        name="Friday",
        sys_prompt="You're a helpful assistant named Friday.",
        model=AnthropicChatModel(
            model_name="glm-4.6",
            api_key=os.environ["GLM_API_KEY"],
            stream=True,
            client_kwargs={"base_url": "https://api.z.ai/api/anthropic"},
        ),
        memory=InMemoryMemory(),
        formatter=AnthropicChatFormatter(),
        toolkit=toolkit,
    )

    user = UserAgent(name="user")

    msg = None
    while True:
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break
        msg = await agent(msg)

asyncio.run(main())
