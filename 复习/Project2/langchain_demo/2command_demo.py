from langgraph.types import Command
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.tools import tool,ToolRuntime

@tool
def clear_conversation() -> Command:
    """Clear the conversation history."""
    return Command(update={"messages":[RemoveMessage(id = REMOVE_ALL_MESSAGES)]})


@tool
def update_user_name(
        new_name: str,
        runtime: ToolRuntime,
) -> Command:
    return Command(update={"user_name":new_name})