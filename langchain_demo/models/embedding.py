import os

from langchain.schema.embeddings import Embeddings
from zhipuai import ZhipuAI


class GLMEmbeddings(Embeddings):
    def __init__(self):
        self.client = ZhipuAI(api_key=os.getenv("Zhipu_API_KEY"))
        self.embedding_size = 1024

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._get_len_safe_embeddings(texts)

    def _get_len_safe_embeddings(self, texts: list[str]) -> list[list[float]]:
        try:
            # 获取embedding响应
            response = self.client.embeddings.create(model="embedding-2", input=texts)
            data = [item.embedding for item in response.data]
            return data
        except Exception as e:
            print(f"Fail to get embeddings, caused by {e}")
            return []
