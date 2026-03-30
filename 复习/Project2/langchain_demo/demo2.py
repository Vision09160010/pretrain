import os
from langchain_deepseek import ChatDeepSeek
from config import settings

model = ChatDeepSeek(
    model = settings.model_name,
    api_key  = settings.api_key,
    api_base = settings.base_url

)
messages = [{"role":"system","content":"你是一个助手"},{"role":"user","content":"你好"}]
response = model.invoke(
    input=messages,
)

print(response.content)