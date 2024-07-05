import os

from llama_index.core.base.embeddings.base import BaseEmbedding
from pydantic import Field
from zhipuai import ZhipuAI


class GLMEmbeddings(BaseEmbedding):
    client = Field(description="embedding model client")
    embedding_size: float = Field(description="embedding size")

    def __init__(self):
        super().__init__(model_name='GLM', embed_batch_size=64)
        self.client = ZhipuAI(api_key=os.getenv("Zhipu_API_KEY"))
        self.embedding_size = 1024

    def _get_query_embedding(self, query: str) -> list[float]:
        return self._get_text_embeddings([query])[0]

    def _get_text_embedding(self, text: str) -> list[float]:
        return self._get_text_embeddings([text])[0]

    def _get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self._get_len_safe_embeddings(texts)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)

    def _get_len_safe_embeddings(self, texts: list[str]) -> list[list[float]]:
        try:
            # 获取embedding响应
            response = self.client.embeddings.create(model="embedding-2", input=texts)
            data = [item.embedding for item in response.data]
            return data
        except Exception as e:
            print(f"Fail to get embeddings, caused by {e}")
            return []
