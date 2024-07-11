"""
coding   : utf-8
@Date    : 2024/7/10
@Author  : Shaobo
@Describe: 
"""
from models.codegeex import CodegeexChatModel

model: CodegeexChatModel


def stream_chat_with_codegeex(request):
    yield from model.stream_chat(request)


def chat_with_codegeex(request):
    return model.chat(request)


def init_model(args):
    global model
    model = CodegeexChatModel(args)
