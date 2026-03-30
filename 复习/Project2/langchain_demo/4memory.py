from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from langchain_openai import ChatOpenAI
from config import settings
from langchain.messages import HumanMessage
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
store = InMemoryStore()
model = ChatOpenAI(model=settings.model_name,api_key=settings.api_key,base_url=settings.base_url)
agent = create_agent(
    model = model,
    tools=[get_user_info,save_user_info],
    store=store,
)
messages1 = {"messages":[HumanMessage(content="保存以下用户: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev")]}
response1 = agent.invoke(messages1)
messages2 = {"messages":[HumanMessage(content="获取用户id为'abc123'的用户信息")]}
response2 = agent.invoke(messages2)

print(response1["messages"][-1].content)
print("-"*80)
print(response2["messages"][-1].content)