import argparse
import json
import os
import re
from typing import Any, Dict, List, Tuple

import gradio as gr
import requests

SYSTEM_PROMPT = {
    "zh": "你是一位智能编程助手，你叫CodeGeeX，你连接着一台电脑，但请注意不能联网。在使用Python解决任务时，你可以运行代码并得到结果，如果运行结果有错误，你需要尽可能对代码进行改进。你可以处理用户上传到电脑上的文件，文件默认存储路径是/mnt/data/。",
    "en": "You are an intelligent programming assistant named CodeGeeX, connected to a computer, but please note that you cannot access the internet. When solving tasks using Python, you can run code and obtain results. If there are any errors in the results, you need to improve the code as much as possible. You can also handle files uploaded to the computer, with the default storage path being /mnt/data/.",
}

CODEGEEX_SPECIAL_TOKENS = {
    "user": "<|user|>",
    "assistant": "<|assistant|>",
    "system": "<|system|>",
    "observation": "<|observation|>",
    "eos": "<|endoftext|>",
}


parser = argparse.ArgumentParser(description="CodeGeeX4 Interpreter")
parser.add_argument("--tgi-addr", type=str, required=True)
parser.add_argument("--sandbox-addr", type=str, default="http://127.0.0.1:8080")
parser.add_argument("--temperature", type=float, default=0.2)
parser.add_argument("--top-p", type=float, default=0.95)
args = parser.parse_args()


code_block_regex = re.compile(r"```(.*?)\n(.*?)```", re.DOTALL)


def execute_code_block(lang, code) -> Tuple[List[Dict[str, Any]], str]:
    assert lang in ["python"]
    response = requests.post(
        f"{args.sandbox_addr}/execute",
        json={"code": code, "timeout_secs": 60},
    )
    response = response.json()
    print(f"[RESPONSE] {response}")
    return response["events"], response["status"]


def upload_file(filepath: str, contents: str):
    print(f"[REQUEST] Upload {filepath} ({len(contents)} bytes)")
    response = requests.post(
        f"{args.sandbox_addr}/files/upload/-/{filepath.lstrip('/')}",
        data=bytes(contents, encoding="utf-8"),
    )
    print(f"[RESPONSE] {response.text}")
    assert response.status_code == 201


def stream_chat_completion(message, history):
    should_stop = False
    round = 0
    max_rounds = 5

    file_info = ""
    for filepath in message.get("files", []):
        with open(filepath, "r") as f:
            contents = f.read()
        filename = os.path.basename(filepath)
        upload_file(f"/mnt/data/{filename}", contents)
        file_info += f"# File: /mnt/data/{filename}\n"
        file_info += f"# Size: {len(contents)}\n"
        file_info += "# File uploaded\n"

    prompt = f"{CODEGEEX_SPECIAL_TOKENS['system']}\n{SYSTEM_PROMPT['en']}\n"
    for [user_message, bot_message] in history:
        if isinstance(user_message, tuple):
            # It's a file
            pass
        else:
            # Remove any '![image](data:image/png;base64,...)' from the bot message.
            bot_message = re.sub(
                r"!\[image\]\(data:image/png;base64,[^\)]+\)", "", bot_message
            )
            prompt += f"{CODEGEEX_SPECIAL_TOKENS['user']}\n{user_message}\n"
            prompt += f"{CODEGEEX_SPECIAL_TOKENS['assistant']}\n{bot_message}\n"
    prompt += f"{CODEGEEX_SPECIAL_TOKENS['user']}\n{file_info}{message['text']}\n"
    prompt += f"{CODEGEEX_SPECIAL_TOKENS['assistant']}\n"

    stop_sequences = [
        CODEGEEX_SPECIAL_TOKENS["eos"],
        CODEGEEX_SPECIAL_TOKENS["user"],
        CODEGEEX_SPECIAL_TOKENS["observation"],
    ]

    while not should_stop and round < max_rounds:
        round += 1
        request_json_body = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2048,
                "do_sample": True,
                "top_p": args.top_p,
                "temperature": args.temperature,
                "stop": stop_sequences,
                "details": True,
                "stream": False,
            },
        }
        print(f"[REQUEST] {request_json_body}")
        response = requests.post(
            f"{args.tgi_addr}/generate_stream",
            json=request_json_body,
            stream=True,
        )

        completion = ""

        for line in response.iter_lines():
            if line:
                event = line.decode("utf-8")
                if event.startswith("data:"):
                    event = event[5:].strip()
                    event = json.loads(event)
                    token = event["token"]["text"]

                    completion += token
                    prompt += token

                    # Only display the token if it's not "special".
                    if event["token"]["text"] not in CODEGEEX_SPECIAL_TOKENS.values():
                        yield token

                    # If the model asks for the code to be executed, do it.
                    if event["token"]["text"] == CODEGEEX_SPECIAL_TOKENS["observation"]:
                        match = code_block_regex.search(completion)
                        if match is None:
                            # Hm, it seems the model didn't write any code.
                            # Let's gently warn it.
                            prompt += f"\n```result\nError: no code to execute.\n```\n{CODEGEEX_SPECIAL_TOKENS['assistant']}\n"
                            yield "```\nError: no code to execute.\n```\n"
                            break

                        lang, code = match.groups()
                        events, status = execute_code_block(lang, code)

                        buffer = []

                        for exec_event in events:
                            if exec_event["type"] == "stream":
                                buffer.append(exec_event["text"])
                            if exec_event["type"] == "display_data":
                                if "text/plain" in exec_event["data"]["variants"]:
                                    buffer.append(
                                        exec_event["data"]["variants"]["text/plain"]
                                    )

                        if status == "timeout":
                            buffer.append("Execution timed out.")
                        if status == "error":
                            buffer.append("Execution failed.")

                        prompt += f"\n```result\n{''.join(buffer)}\n```\n{CODEGEEX_SPECIAL_TOKENS['assistant']}\n"
                        yield f"```\n{''.join(buffer)}\n```\n"

                        for exec_event in events:
                            if exec_event["type"] == "display_data":
                                if "image/png" in exec_event["data"]["variants"]:
                                    yield f"![image](data:image/png;base64,{exec_event['data']['variants']['image/png']})"
                                elif "text/html" in exec_event["data"]["variants"]:
                                    yield exec_event["data"]["variants"]["text/html"]

                        break

                    # If the model otherwise ends the generation, stop here.
                    if event["details"] is not None:
                        should_stop = True
                        break

        print(f"[RESPONSE] {completion}")


def predict(message: Dict[str, Any], history: List[List[str | None | tuple]]):
    completion = ""
    for delta in stream_chat_completion(message, history):
        completion += delta
        # Replace (sandbox:/ by (<sandbox-address>/
        completion = completion.replace(
            "sandbox:/", f"{args.sandbox_addr}/files/download/-/"
        )
        yield completion


demo = gr.ChatInterface(
    fn=predict,
    title="CodeGeeX4 Interpreter",
    description="",
    examples=[
        {"text": "Compute factorial of 21 using code", "files": []},
        {
            "text": "Plot the class distribution of this dataset",
            "files": ["./data.csv"],
        },
        {
            "text": 'Reverse the following string and save it to a file: "9738426487936"',
            "files": [],
        },
    ],
    multimodal=True,
)

demo.launch()
