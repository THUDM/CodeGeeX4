from pydantic import Field
from transformers import AutoModel, AutoTokenizer
from typing import Iterator
import torch
class StreamProcessor:
    def __init__(self):
        self.previous_str = ""

    def get_new_part(self, new_str):
        new_part = new_str[len(self.previous_str):]
        self.previous_str = new_str
        return new_part
class CodegeexChatModel():
    device: str = Field(description="device to load the model")
    tokenizer = Field(description="model's tokenizer")
    model = Field(description="Codegeex model")
    temperature: float = Field(description="temperature to use for the model.")

    def __init__(self,model_name_or_path):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            model_name_or_path,
            trust_remote_code=True
        ).to(self.device).eval()
        print("Model has been initialized.")

    def chat(self, prompt,temperature=0.2,top_p=0.95):
        try:
            response, _ = self.model.chat(
                self.tokenizer,
                query=prompt,
                max_length=4012,
                temperature=temperature,
                top_p=top_p
            )
            return response
        except Exception as e:
            return f"error:{e}"

    def stream_chat(self,prompt,temperature=0.2,top_p=0.95):

        try:
            stream_processor = StreamProcessor()
            for response, _ in self.model.stream_chat(
                    self.tokenizer,
                    query=prompt,
                    max_length=4012,
                    temperature=temperature,
                    top_p=top_p
            ):
                yield stream_processor.get_new_part(response)
        except Exception as e:
            yield f'error: {e}'