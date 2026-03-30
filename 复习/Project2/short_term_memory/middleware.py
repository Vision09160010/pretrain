from langchain.agents import create_agent,AgentState
from langchain.tools import tool,ToolRuntime
from langchain_openai import ChatOpenAI
from config import settings
from langchain.messages import HumanMessage
class CustomState(AgentState):
    user_id: str

@ tool
def get_user_info(runtime:ToolRuntime) -> str:
    """
    查询用户信息
    :param runtime:
    :return:
    """
    user_id = runtime.state["user_id"]
    return "User is John Smith" if user_id == "user_123" else "Unknown user"

model = ChatOpenAI(model = settings.model_name,api_key=settings.api_key,base_url=settings.base_url)
agent = create_agent(
    model = model,
    tools=[get_user_info],
    state_schema=CustomState
)

result = agent.invoke({
    "messages":"查询用户的信息",
    "user_id":"user_123"
})
print(result["messages"][-1].content)