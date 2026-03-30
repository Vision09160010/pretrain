from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from config import settings
model = ChatOpenAI(
    model=settings.model_name,
    api_key=settings.api_key,
    base_url=settings.base_url,
)

agent = create_agent(
    model=model,
)
messages = {"messages":[SystemMessage(content="你是小隹，是一个心理理疗师"),HumanMessage(content="你好")]}
response = agent.invoke(
    input=messages
)

print(response["messages"][-1].content)