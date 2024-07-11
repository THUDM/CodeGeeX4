"""
coding   : utf-8
@Date    : 2024/7/10
@Author  : Shaobo
@Describe: 
"""

import torch
from protocols.openai_api import ChatCompletionRequest, ChatCompletionStreamResponse, ChatCompletionResponse
from sseclient import Event
from transformers import AutoTokenizer, AutoModel


class CodegeexChatModel:
    def __init__(self, args):
        self.tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
        if args.bf16:
            self.model = AutoModel.from_pretrained(
                args.model_name_or_path,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16,
            ).to(args.device).eval()
        else:
            self.model = AutoModel.from_pretrained(
                args.model_name_or_path,
                trust_remote_code=True
            ).to(args.device).eval()
        print("Model is initialized.")

    def stream_chat(self, request: ChatCompletionRequest):
        try:
            length = 0
            for i, (response, _) in enumerate(self.model.stream_chat(
                    self.tokenizer,
                    query=request.messages[-1].content,
                    history=[msg.model_dump() for msg in request.messages[:-1]],
                    max_new_tokens=request.max_tokens,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    repetition_penalty=request.presence_penalty
            )):
                resp = ChatCompletionStreamResponse()
                resp.choices[0].index = i
                resp.choices[0].delta.content = response[length:]
                event = Event(id=resp.id, data=resp.json(), event='message')
                yield event.dump()
                length = len(response)
            resp = ChatCompletionStreamResponse()
            resp.choices[0].finish_reason = 'stop'
            event = Event(id=resp.id, data=resp.json(), event='message')
            yield event.dump()
        except Exception as e:
            resp = ChatCompletionStreamResponse()
            resp.choices[0].finish_reason = 'stop'
            event = Event(id=resp.id, data=f"请求报错，错误原因：{e}", event='message')
            yield event.dump()

    def chat(self, request: ChatCompletionRequest):
        try:
            response, _ = self.model.chat(
                self.tokenizer,
                query=request.messages[-1].content,
                history=[msg.model_dump() for msg in request.messages[:-1]],
                max_new_tokens=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                repetition_penalty=request.presence_penalty
            )
            resp = ChatCompletionResponse()
            resp.choices[0].message.content = response
            resp.choices[0].finish_reason = 'stop'
            return resp.model_dump()
        except Exception as e:
            return f"请求报错，错误原因：{e}"
