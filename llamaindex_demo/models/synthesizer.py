from llama_index.core.response_synthesizers import BaseSynthesizer

from models.codegeex import CodegeexChatModel
from utils.prompts import CUSTOM_PROMPT_TEMPLATE


class CodegeexSynthesizer(BaseSynthesizer):
    """Response builder class."""

    def __init__(self, args) -> None:
        super().__init__(llm=CodegeexChatModel(args))
        self.prompt_template = CUSTOM_PROMPT_TEMPLATE

    def get_response(self, query_str: str, text_chunks: list[str], **kwargs) -> str:
        context = self.build_context(text_chunks)
        return self._llm.predict(self.prompt_template, query=query_str, context=context)

    async def aget_response(self, query_str: str, text_chunks: list[str], **kwargs) -> str:
        context = self.build_context(text_chunks)
        return await self._llm.apredict(self.prompt_template, query=query_str, context=context)

    def _get_prompts(self):
        """Get prompts."""
        return {"text_qa_template": self.prompt_template}

    def _update_prompts(self, prompts) -> None:
        """Update prompts."""
        if "text_qa_template" in prompts:
            self.prompt_template = prompts["text_qa_template"]

    @staticmethod
    def build_context(text_chunks):
        """
        merge contexts
        :param text_chunks: recalled texts
        """
        return "\n\n".join(
            [f"[[citation:{i + 1}]]\n```markdown\n{chunk}\n```" for i, chunk in enumerate(text_chunks)]
        )
