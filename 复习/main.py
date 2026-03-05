from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage,SystemMessage,AIMessage
from conf import settings
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
config = {"configurable":{"thread_id":"1"}}
model = ChatDeepSeek(
    model=settings.deepseek_chat_model,
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url,
)
@tool
def tool1(a,b):
    """
    计算a+b的值的工具
    :param a: 参数a
    :param b: 参数b
    :return: 计算a+b的值
    """
    return a+b

agent = create_agent(
    model = model,
    tools=[tool1],
    checkpointer=checkpointer

)



while True:
    messages = {
        "messages":
            [
                SystemMessage(content="你是一个智能助手"),
                HumanMessage(content=input("请输入query: ")),

            ]
    }
    response = agent.invoke(input=messages,config=config)
    print(response["messages"][-1].content)

# print("-"*50)
