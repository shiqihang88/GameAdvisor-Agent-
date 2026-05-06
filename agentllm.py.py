from openai import OpenAI
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
import json

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

def chat(messages, tools=None):
    """调用大模型，支持 tool calling"""
    kwargs = dict(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.1,
    )
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message