"""
coding   : utf-8
@Date    : 2024/7/10
@Author  : Shaobo
@Describe: 
"""
import argparse

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from protocols.openai_api import ChatCompletionRequest
from services.chat import init_model, chat_with_codegeex, stream_chat_with_codegeex

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="THUDM/codegeex4-all-9b")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--bf16", type=bool, default=False)
    return parser.parse_args()


@app.post("/v1/chat/completions")
async def chat(request: ChatCompletionRequest):
    try:
        if request.stream:
            return StreamingResponse(stream_chat_with_codegeex(request), media_type="text/event-stream")
        else:
            return JSONResponse(chat_with_codegeex(request))
    except Exception as e:
        return JSONResponse(e, status_code=500)


if __name__ == "__main__":
    args = parse_arguments()
    init_model(args)
    uvicorn.run(app, host="127.0.0.1", port=8080)
