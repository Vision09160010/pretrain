from openai import OpenAI
from config import settings


client = OpenAI(api_key=settings.api_key,
       base_url=settings.base_url)


messages = [{"role":"system","content":"你是小隹，是一个心理理疗师"},{"role":"user","content":"你好"}]
response = client.chat.completions.create(
    model = settings.model_name,
    messages=messages,
)

print(response.choices[0].message.content)