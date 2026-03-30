from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.config import get_stream_writer
from config import settings

model = ChatOpenAI(model=settings.model_name,api_key=settings.api_key,base_url=settings.base_url)
def get_weather(city:str)->str:
    """获取给定城市的天气。"""
    writer = get_stream_writer()
    writer(f"Looking up data for city:{city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"


agent = create_agent(
    model=model,
    tools=[get_weather]
)
messages = {"messages":[HumanMessage("北京的天气怎么样?")]}
for stream_mode,chunk in agent.stream(
    messages,
    stream_mode=["updates","custom"]
):
    print(f"stream_mode: {stream_mode}")
    print(f"content: {chunk}")
    print('\n')