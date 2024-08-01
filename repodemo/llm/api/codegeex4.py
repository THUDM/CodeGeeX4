import json
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
# 加载 .env 文件
load_dotenv()
def codegeex4(messages_list, temperature=0.2, top_p=0.95):
    openai_api_key = os.getenv("openai_api_key")
    openai_api_base = os.getenv("openai_api_base")
    model_name = os.getenv("model_name")

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
 
    chat_response = client.chat.completions.create(
        model=model_name,
        messages=messages_list,
        temperature =temperature,
        top_p=top_p,
        max_tokens=8192
    )
    return chat_response.choices[0].message.content


