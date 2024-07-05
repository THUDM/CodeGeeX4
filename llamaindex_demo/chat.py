"""
References: https://docs.llamaindex.ai/en/stable/use_cases/q_and_a/
"""
import argparse

import gradio as gr
from llama_index.core import Settings

from models.embedding import GLMEmbeddings
from models.synthesizer import CodegeexSynthesizer
from utils.vector import load_vectors


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vector_path', type=str, help="path to store the vectors", default='vectors')
    parser.add_argument('--model_name_or_path', type=str, default='THUDM/codegeex4-all-9b')
    parser.add_argument('--device', type=str, help="cpu or cuda", default="cpu")
    parser.add_argument('--temperature', type=float, help="model's temperature", default=0.2)
    return parser.parse_args()


def chat(query, history):
    resp = query_engine.query(query)

    ans = "相关文档".center(150, '-') + '\n'
    yield ans
    for i, node in enumerate(resp.source_nodes):
        file_name = node.metadata['filename']
        ext = node.metadata['extension']
        text = node.text
        ans += f"File{i + 1}: {file_name}\n```{ext}\n{text}\n```\n"
        yield ans

    ans += "模型回复".center(150, '-') + '\n'
    ans += resp.response
    yield ans


if __name__ == '__main__':
    args = parse_arguments()
    Settings.embed_model = GLMEmbeddings()
    try:
        query_engine = load_vectors(args.vector_path).as_query_engine(
            response_synthesizer=CodegeexSynthesizer(args)
        )
    except Exception as e:
        print(f"Fail to load vectors, caused by {e}")
        exit()
    demo = gr.ChatInterface(chat).queue()
    demo.launch(server_name="127.0.0.1", server_port=8080)
