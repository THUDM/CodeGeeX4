import json

from backend.apis.api import API
from backend.apis.bing import BingSearchAPI
from backend.models.codegeex import model, tokenizer
from backend.utils.chat import build_model_input, SYS_PROMPT


def chat(query: str, history: list[list[str]] = None):
    if not history:
        history = []

    ans = ""

    # Search with bing
    api: API = BingSearchAPI()
    search_res = api.call(query=query, history=history)
    ans += "搜索结果".center(100, "-") + '\n'
    ans += "```json\n" + json.dumps(search_res, indent=4, ensure_ascii=False) + "\n```\n"
    yield ans

    # Build model's input
    inputs: str = build_model_input(query, search_res)

    # Generate response
    ans += "模型回复".center(100, "-") + '\n'
    yield ans
    response, _ = model.chat(
        tokenizer,
        query=inputs,
        history=[{"role": "system", "content": SYS_PROMPT}],
        max_new_tokens=1024,
        temperature=0.2
    )
    yield ans + response
