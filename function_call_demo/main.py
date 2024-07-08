import json
import re
from json import JSONDecodeError

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name_or_path = "THUDM/codegeex4-all-9b"
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True
    ).to(device).eval()

    tool_content = {
        "function": [
            {
                "name": "weather",
                "description": "Use for searching weather at a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "description": "the location need to check the weather",
                            "type": "str",
                        }
                    },
                    "required": [
                        "location"
                    ]
                }
            }
        ]
    }
    response, _ = model.chat(
        tokenizer,
        query="Tell me about the weather in Beijing",
        history=[{"role": "tool", "content": tool_content}],
        max_new_tokens=1024,
        temperature=0.1
    )

    # support parallel calls, thus the result is a list
    functions = post_process(response)
    try:
        return [json.loads(func) for func in functions if func]
    # get rid of some possible invalid formats
    except JSONDecodeError:
        try:
            return [json.loads(func.replace('(', '[').replace(')', ']')) for func in functions if func]
        except JSONDecodeError:
            try:
                return [json.loads(func.replace("'", '"')) for func in functions if func]
            except JSONDecodeError as e:
                return [{"answer": response, "errors": e}]


def post_process(text: str) -> list[str]:
    """
    Process model's response.
    In case there are parallel calls, each call is warpped with ```json```.
    """
    pattern = r'```json(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


if __name__ == '__main__':
    output = main()
    print(output)  # [{"name": "weather", "arguments": {"location": "Beijing"}}]
