from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from config import settings
from langchain.agents import create_agent
model = ChatOpenAI(
    model=settings.model_name,
    base_url=settings.base_url,
    api_key=settings.api_key
)
def get_weather(city:str) -> str:
    """获取给定城市的天气"""
    return f"今天{city}是晴天"


messages = {"messages":[HumanMessage("北京的天气怎么样?")]}

agent = create_agent(model,
                     tools=[get_weather],
                     )
for token,metadata in agent.stream(
    input=messages,
    stream_mode="messages"
):
    print(f"node: {metadata['langgraph_node']}")
    print(f"content: {token.content_blocks}")
    print("\n")