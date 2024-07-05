from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms import LLM
from pydantic import Field
from transformers import AutoTokenizer, AutoModel

from utils.prompts import SYS_PROMPT


class CodegeexChatModel(LLM):
    device: str = Field(description="device to load the model")
    tokenizer = Field(description="model's tokenizer")
    model = Field(description="Codegeex model")
    temperature: float = Field(description="temperature to use for the model.")

    def __init__(self, args):
        super().__init__()
        self.device = args.device
        self.tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(args.model_name_or_path, trust_remote_code=True).to(args.device).eval()
        self.temperature = args.temperature
        print("Model has been initialized.")

    @classmethod
    def class_name(cls) -> str:
        return "codegeex"

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=7168,
            num_output=1024,
            is_chat_model=True,
            model_name="codegeex",
        )

    def chat(self, messages: list[ChatMessage], **kwargs) -> ChatResponse:
        try:
            response, _ = self.model.chat(
                self.tokenizer,
                query=messages[0].content,
                history=[{"role": "system", "content": SYS_PROMPT}],
                max_new_tokens=1024,
                temperature=self.temperature
            )
            return ChatResponse(message=ChatMessage(role="assistant", content=response))
        except Exception as e:
            return ChatResponse(message=ChatMessage(role="assistant", content=e))

    def stream_chat(self, messages: list[ChatMessage], **kwargs) -> ChatResponseGen:

        try:
            for response, _ in self.model.stream_chat(
                    self.tokenizer,
                    query=messages[0].content,
                    history=[{"role": "system", "content": SYS_PROMPT}],
                    max_new_tokens=1024,
                    temperature=self.temperature
            ):
                yield ChatResponse(message=ChatMessage(role="assistant", content=response))
        except Exception as e:
            yield ChatResponse(message=ChatMessage(role="assistant", content=e))

    def complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponse:
        try:
            response, _ = self.model.chat(
                self.tokenizer,
                query=prompt,
                history=[{"role": "system", "content": "你是一个智能编程助手"}],
                max_new_tokens=1024,
                temperature=self.temperature
            )
            return CompletionResponse(text=response)
        except Exception as e:
            return CompletionResponse(text=e)

    def stream_complete(self, prompt: str, formatted: bool = False, **kwargs) -> CompletionResponseGen:
        try:
            for response, _ in self.model.stream_chat(
                    self.tokenizer,
                    query=prompt,
                    history=[{"role": "system", "content": "你是一个智能编程助手"}],
                    max_new_tokens=1024,
                    temperature=self.temperature
            ):
                yield CompletionResponse(text=response)
        except Exception as e:
            yield CompletionResponse(text=e)

    async def achat(self, messages: list[ChatMessage], **kwargs):
        return await self.chat(messages, **kwargs)

    async def astream_chat(self, messages: list[ChatMessage], **kwargs):
        async for resp in self.stream_chat(messages, **kwargs):
            yield resp

    async def acomplete(self, prompt: str, formatted: bool = False, **kwargs):
        return await self.complete(prompt, formatted, **kwargs)

    async def astream_complete(self, prompt: str, formatted: bool = False, **kwargs):
        async for resp in self.stream_complete(prompt, formatted, **kwargs):
            yield resp
