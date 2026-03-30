from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool,ToolRuntime
from config import settings
from langchain.messages import HumanMessage
USER_DATABASE = {
    "user123":{
        "name":"Alice Johnson",
        "account_type": "Premium",
        "balance": 5000,
        "email": "alice@example.com"
    },
    "user456": {
        "name": "Bob Smith",
        "account_type": "Standard",
        "balance": 1200,
        "email": "bob@example.com"
    },
}

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's account information."""
    user_id = runtime.context.user_id
    if user_id in USER_DATABASE:
        user = USER_DATABASE[user_id]
        return f"Account holder:{user['name']}\nType: {user['account_type']}\nBalance: ${user['balance']}"
    return "User not found"

model = ChatOpenAI(model=settings.model_name,api_key=settings.api_key,base_url=settings.base_url)
aagent = create_agent(model=model,
                      tools=[get_account_info],
                      context_schema=UserContext,
                      system_prompt="你是一个财务助手."
                      )
messages = {"messages":[HumanMessage(content="我当前的余额是多少？")]}
response = aagent.invoke(input = messages,context=UserContext(user_id="user123"))
print(response["messages"][-1].content)
