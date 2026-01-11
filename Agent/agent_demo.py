from langgraph.graph import StateGraph,END,START
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from conf import settings
from typing import List,TypedDict,Dict
from langgraph.checkpoint.memory import InMemorySaver
# 添加到数据库



checkpointer = InMemorySaver()
model = ChatOpenAI(
    model = settings.model_name,
    base_url = settings.base_url,
    api_key = settings.api_key,
)

class State(TypedDict):
    messages:List[Dict[str,str]]


agent = create_agent(
    model = model,
    tools = [],
    checkpointer = checkpointer,
)


agent1 = agent.invoke(
    {"messages": [{"role": "user", "content": "你好,我叫张三，请记住我的名字"}]},
    config = {"thread_id": "1"},
)

agent2 = agent.invoke(
    {"messages": [{"role": "user", "content": "你好，我叫王五"}]},
    config = {"thread_id": "2"},
)

agent3 = agent.invoke(
    {"messages": [{"role": "user", "content": "你好,我叫什么"}]},
    config = {"thread_id": "1"},
)

