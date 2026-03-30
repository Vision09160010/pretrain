from langchain.tools import tool,ToolRuntime


@tool
def summarize_conversation(
        runtime: ToolRuntime,
) -> str:
    """summarize the conversation so far"""
    messages = runtime.state["messages"]
    human_msgs = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_msgs = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_msgs = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")
    return f"Conversation has {human_msgs} user messages, {ai_msgs} AI responses,  and {tool_msgs} tool results"

@tool
def get_user_preference(pref_name:str,  runtime: ToolRuntime) -> str:
    """get a user preference value."""
    preferences = runtime.state.get("preferences",{})
    return preferences.get(pref_name,"Not set")