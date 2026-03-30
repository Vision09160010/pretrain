from langchain.agents import create_agent
from config import settings
from langchain_openai import ChatOpenAI
from typing import Any
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool,ToolRuntime
from langchain.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
@tool
def get_user_info(user_id:str,runtime:ToolRuntime) -> str:
    """查看用户信息"""
    store = runtime.store
    user_info = store.get(("users",),user_id)
    return str(user_info.value) if user_info else "Unknown user"

@tool
def save_user_info(user_id:str,user_info:dict[str,Any],runtime:ToolRuntime) -> str:
    """保存用户信息"""
    store = runtime.store
    store.put(("users",),user_id,user_info)
    return "成功保存用户信息。"

model = ChatOpenAI(model=settings.model_name,api_key=settings.api_key,base_url=settings.base_url)
agent = create_agent(
    model = model,
    tools=[get_user_info],
    checkpointer = InMemorySaver()
)


DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    checkpointer.setup()


messages = {"messages":[HumanMessage(content="你好，我的名字是vision")]}
configurable = {"configurable":{"thread_id":"1"}}
response = agent.invoke(
    input = messages,
    tool = [get_user_info],
    config=configurable,
)

print(response["messages"])