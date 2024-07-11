"""
coding   : utf-8
@Date    : 2024/7/11
@Author  : Shaobo
@Describe: 
"""
import time
from typing import Literal

import shortuuid
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "codegeex4"
    messages: list[ChatMessage]
    temperature: float = 0.2
    top_p: float = 1.0
    max_tokens: int = 1024
    stop: list[str] = ['<|user|>', '<|assistant|>', '<|observation|>', '<|endoftext|>']
    stream: bool = True
    presence_penalty: float = None


class DeltaMessage(BaseModel):
    role: str
    content: str


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int = 0
    delta: DeltaMessage = DeltaMessage(role='assistant', content='')
    finish_reason: Literal["stop", "length"] = None


class ChatCompletionStreamResponse(BaseModel):
    id: str = f"chatcmpl-{shortuuid.random()}"
    object: str = "chat.completion.chunk"
    created: int = int(time.time())
    model: str = "codegeex4"
    choices: list[ChatCompletionResponseStreamChoice] = [ChatCompletionResponseStreamChoice()]


class ChatCompletionResponseChoice(BaseModel):
    index: int = 0
    message: ChatMessage = ChatMessage(role="assistant", content="")
    finish_reason: Literal["stop", "length"] = None


class ChatCompletionResponse(BaseModel):
    id: str = f"chatcmpl-{shortuuid.random()}"
    object: str = "chat.completion"
    created: int = int(time.time())
    model: str = "codegeex4"
    choices: list[ChatCompletionResponseChoice] = [ChatCompletionResponseChoice()]
    # usage: UsageInfo
