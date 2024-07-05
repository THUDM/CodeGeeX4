from typing import Iterator

import torch
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk, ChatResult, ChatGeneration
from pydantic import Field
from transformers import AutoModel, AutoTokenizer
from utils.prompts import SYS_PROMPT


class CodegeexChatModel(BaseChatModel):
    device: str = Field(description="device to load the model")
    tokenizer = Field(description="model's tokenizer")
    model = Field(description="Codegeex model")
    temperature: float = Field(description="temperature to use for the model.")

    def __init__(self, args):
        super().__init__()
        self.device = args.device
        self.tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            args.model_name_or_path,
            trust_remote_code=True
        ).to(args.device).eval()
        self.temperature = args.temperature
        print("Model has been initialized.")

    def _llm_type(self) -> str:
        return "codegeex"

    @torch.inference_mode()
    def _generate(self, messages, **kwargs):
        try:
            response, _ = self.model.chat(
                self.tokenizer,
                query=messages[0].content,
                history=[{"role": "system", "content": SYS_PROMPT}],
                max_new_tokens=1024,
                temperature=self.temperature
            )
            return ChatResult(generations=[ChatGeneration(message=BaseMessage(content=response, type='ai'))])
        except Exception as e:
            return ChatResult(generations=[ChatGeneration(message=BaseMessage(content=repr(e), type='ai'))])

    def _stream(self, messages: list[BaseMessage], **kwargs) -> Iterator[ChatGenerationChunk]:
        try:
            for response, _ in self.model.stream_chat(
                    self.tokenizer,
                    query=messages[0].content,
                    history=[{"role": "system", "content": SYS_PROMPT}],
                    max_new_tokens=1024,
                    temperature=self.temperature
            ):
                yield ChatGenerationChunk(message=AIMessageChunk(content=response))
        except Exception as e:
            yield ChatGenerationChunk(message=AIMessageChunk(content=f"Fail to generate, cause by {e}"))
