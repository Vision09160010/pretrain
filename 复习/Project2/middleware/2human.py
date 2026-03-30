from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from openai import api_key
from langchain.tools import tool,ToolRuntime


@tool
def read_email_tool():
    return None
@tool
def send_email_tool():
    return None


from config import settings
model = ChatOpenAI(model=settings.model_name,base_url=settings.base_url,api_key=settings.api_key)
agent =  create_agent(
    model=model,
    tools=[read_email_tool,send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # 要求发邮件进行批准、编辑或拒绝
                "send_email_tool": {
                    "allowed_decisions":["approve", "edit", "reject"],
                },
                "read_email_tool": False,
            }
        )
    ]
)