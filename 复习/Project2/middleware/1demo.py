from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from config import settings
from langchain.agents.middleware import SummarizationMiddleware,HumanInTheLoopMiddleware
model = ChatOpenAI(model=settings.model_name,base_url=settings.base_url,api_key=settings.api_key)
agent = create_agent(
    model = model,
    middleware=[SummarizationMiddleware(
        model = model,
        max_tokens_before_summary=4000,
        messages_to_keep=20,
        summary_prompt="请总结上述内容"
    )]
)