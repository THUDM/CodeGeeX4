"""
References: https://python.langchain.com/v0.2/docs/tutorials/rag/
"""
import argparse

import gradio as gr
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from models.codegeex import CodegeexChatModel
from utils.prompts import CUSTOM_RAG_PROMPT
from utils.vector import load_vector_store


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vector_path', type=str, help="path to load the vectors", default='vectors')
    parser.add_argument('--model_name_or_path', type=str, default='THUDM/codegeex4-all-9b')
    parser.add_argument('--device', type=str, help="cpu or cuda", default="cpu")
    parser.add_argument('--temperature', type=float, help="model's temperature", default=0.2)
    return parser.parse_args()


def format_docs(docs):
    return "\n\n".join(
        [f"[[citation:{i + 1}]]\n```markdown\n{doc.page_content}\n```" for i, doc in enumerate(docs)]
    )


def chat(query, history):
    retrieve_chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()} | CUSTOM_RAG_PROMPT)
    retrieve_output = retrieve_chain.invoke(query)

    ans = retrieve_output.text
    yield ans

    ans += "模型回复".center(150, '-') + '\n'
    yield ans

    parse_chain = (llm | StrOutputParser())
    ans += parse_chain.invoke(retrieve_output)
    yield ans


if __name__ == '__main__':
    args = parse_arguments()
    llm = CodegeexChatModel(args)
    try:
        retriever = load_vector_store(args.vector_path).as_retriever()
    except Exception as e:
        print(f"Fail to load vectors，caused by {e}")
        exit()
    demo = gr.ChatInterface(chat).queue()
    demo.launch(server_name="127.0.0.1", server_port=8080)
