from typing import Annotated
from langchain.agents import create_agent,AgentState
from langchain.tools import InjectedToolCallId
from langchain.tools import tool,ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage,HumanMessage
from config import settings
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model=settings.model_name,api_key=settings.api_key,base_url=settings.base_url)

subagent1 = create_agent(model)

class CustomState(AgentState):
    example_state_key: str


@tool(
    "subagent1_name",
    description="subagent1_description"
)
def call_subagent_1(query: str,tool_call_id: Annotated[str,InjectedToolCallId]) -> Command:
    result = subagent1.invoke({
        "messages":[{"role":"user","content":query}]
    })
    return Command(update={
        "example_state_key": result["example_state_key"],
        "messages": [
            ToolMessage(
                content=result["messages"][-1].content,
                # 我们需要包含工具调用 ID，以便它与正确的工具调用匹配
                tool_call_id=tool_call_id
            )
        ]
    })

agent = create_agent(model,tools=[call_subagent_1])
messages = {"messages":[
    HumanMessage("有你管理的子智能体吗")
]}
result = agent.invoke(messages)
print(result["messages"][-1].content)


