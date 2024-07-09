import chainlit as cl
from chainlit.input_widget import Slider
from llm.api.codegeex4 import codegeex4
from prompts.base_prompt import (
    judge_task_prompt,
    get_cur_base_user_prompt,
    web_judge_task_prompt,
)
from utils.tools import unzip_file, get_project_files_with_content
from utils.bingsearch import bing_search_prompt
from llm.local.codegeex4 import CodegeexChatModel

local_model_path = "<your_local_model_path>"
llm = CodegeexChatModel(local_model_path)


class StreamProcessor:
    def __init__(self):
        self.previous_str = ""

    def get_new_part(self, new_str):
        new_part = new_str[len(self.previous_str) :]
        self.previous_str = new_str
        return new_part


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="chat聊天",
            markdown_description="聊天demo：支持多轮对话。",
            starters=[
                cl.Starter(
                    label="请你用python写一个快速排序。",
                    message="请你用python写一个快速排序。",
                ),
                cl.Starter(
                    label="请你介绍一下自己。",
                    message="请你介绍一下自己。",
                ),
                cl.Starter(
                    label="用 Python 编写一个脚本来自动发送每日电子邮件报告，并指导我如何进行设置。",
                    message="用 Python 编写一个脚本来自动发送每日电子邮件报告，并指导我如何进行设置。",
                ),
                cl.Starter(
                    label="我是一个python初学者，请你告诉我怎么才能学好python。",
                    message="我是一个python初学者，请你告诉我怎么才能学好python。",
                ),
            ],
        ),
        cl.ChatProfile(
            name="联网问答",
            markdown_description="联网能力demo：支持联网回答用户问题。",
        ),
        cl.ChatProfile(
            name="上传本地项目",
            markdown_description="项目级能力demo：支持上传本地zip压缩包项目，可以进行项目问答和对项目进行修改。",
        ),
    ]


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Slider(
                id="temperature",
                label="CodeGeeX4 - Temperature",
                initial=0.2,
                min=0,
                max=1,
                step=0.1,
            ),
            Slider(
                id="top_p",
                label="CodeGeeX4 - top_p",
                initial=0.95,
                min=0,
                max=1,
                step=0.1,
            ),
        ]
    ).send()
    temperature = settings["temperature"]
    top_p = settings["top_p"]
    cl.user_session.set("temperature", temperature)
    cl.user_session.set("top_p", top_p)
    cl.user_session.set("message_history", [])
    chat_profile = cl.user_session.get("chat_profile")
    extract_dir = "repodata"
    if chat_profile == "chat聊天":
        pass
    elif chat_profile == "上传本地项目":
        files = None
        while files == None:
            files = await cl.AskFileMessage(
                content="请上传项目zip压缩文件!",
                accept={"application/zip": [".zip"]},
                max_size_mb=50,
            ).send()

        text_file = files[0]
        extracted_path = unzip_file(text_file.path, extract_dir)
        files_list = get_project_files_with_content(extracted_path)
        cl.user_session.set("project_index", files_list)
        if len(files_list) > 0:
            await cl.Message(
                content=f"已成功上传，您可以开始对项目进行提问！",
            ).send()


@cl.on_message
async def main(message: cl.Message):
    chat_profile = cl.user_session.get("chat_profile")
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    if chat_profile == "chat聊天":
        prompt_content = get_cur_base_user_prompt(message_history=message_history)

    elif chat_profile == "联网问答":
        judge_context = llm.chat(
            web_judge_task_prompt.format(user_input=message.content), temperature=0.2
        )
        print(judge_context)
        message_history.pop()

        if "是" in judge_context:
            prompt_tmp = bing_search_prompt(message.content)
            message_history.append({"role": "user", "content": prompt_tmp})
        else:
            message_history.append({"role": "user", "content": message.content})
        prompt_content = get_cur_base_user_prompt(message_history=message_history)

    elif chat_profile == "上传本地项目":
        judge_context = llm.chat(
            judge_task_prompt.format(user_input=message.content), temperature=0.2
        )

        project_index = cl.user_session.get("project_index")
        index_prompt = ""
        index_tmp = """###PATH:{path}\n{code}\n"""
        for index in project_index:
            index_prompt += index_tmp.format(path=index["path"], code=index["content"])
        print(judge_context)
        prompt_content = (
            get_cur_base_user_prompt(
                message_history=message_history,
                index_prompt=index_prompt,
                judge_context=judge_context,
            )
            if "正常" not in judge_context
            else get_cur_base_user_prompt(message_history=message_history)
        )

    msg = cl.Message(content="")
    await msg.send()
    temperature = cl.user_session.get("temperature")
    top_p = cl.user_session.get("top_p")

    if len(prompt_content) / 4 < 120000:
        stream = llm.stream_chat(prompt_content, temperature=temperature, top_p=top_p)
        stream_processor = StreamProcessor()
        for part in stream:
            if isinstance(part, str):
                text = stream_processor.get_new_part(part)
            elif isinstance(part, dict):
                text = stream_processor.get_new_part(part["name"] + part["content"])
            if token := (text or " "):
                await msg.stream_token(token)
    else:
        await msg.stream_token("项目太大了，请换小一点的项目。")

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
