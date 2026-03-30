from langchain.tools import tool,ToolRuntime
from langchain_core.messages import HumanMessage
from langchain.messages import ToolMessage
from langchain.agents import create_agent,AgentState
from langgraph.types import Command
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from config import settings
model = ChatOpenAI(model=settings.model_name,base_url=settings.base_url,api_key=settings.api_key)

class CustomState(AgentState):
    user_name: str

class CustomContext(BaseModel):
    user_id: str

@tool
def update_user_info(runtime: ToolRuntime[CustomContext,CustomState]) -> Command:
    """查找并更新用户信息"""
    user_id = runtime.context.user_id
    name = "John Smith" if user_id == "user_123" else "Unknown user"
    return Command(update={
        "user_name":name,
        "messages":[
            ToolMessage(
                "Successfully looked up user information",
                tool_call_id = runtime.tool_call_id
            )
        ]
    })
@tool
def greet(runtime: ToolRuntime[CustomContext,CustomState]) -> str:
    """Use this to greet the user once you found their info."""
    user_name = runtime.state["user_name"]
    return f"Hello {user_name}!"

agent = create_agent(
    model=model,
    tools=[update_user_info,greet],
    state_schema=CustomState,
    context_schema=CustomContext,
)
inputs = {"messages":[
    HumanMessage(content="greet the user")
]}
results = agent.invoke(
    input=inputs,
    context=CustomContext(user_id="user_123"),
)

print(results["messages"][-1].content)