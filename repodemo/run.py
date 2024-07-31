import chainlit as cl
from chainlit.input_widget import Slider,Switch
import json
import re

from llm.api.codegeex4 import codegeex4
from prompts.base_prompt import (
    get_cur_base_user_prompt,
    build_message_list,
    tools_choose_prompt,
    tools_input_prompt
)
from utils.bingsearch import bing_search_prompt
from utils.tools import unzip_file, get_project_files_with_content,clone_repo,is_valid_json

def tools_choose_agent(input_text):
    tools_prompt = tools_choose_prompt+tools_input_prompt.format(input_text=input_text)
    message_list = build_message_list(tools_prompt)
    judge_tmp = codegeex4(
        messages_list=message_list,
        temperature=0.2,
        top_p=0.95,
    )
    judge_context = ""
    for part in judge_tmp:
        judge_context += part
    attempt = 1
    max_attempts = 10
    while not is_valid_json(judge_context) and attempt <= max_attempts:
        judge_tmp = codegeex4(
            messages_list=message_list,
            temperature=0.2,
            top_p=0.95,
        )
        judge_context = ""
        for part in judge_tmp:
            judge_context += part
        attempt += 1
    match = re.search(r'\{.*\}', judge_context, re.DOTALL)
    if match:
        dict_str = match.group()
        response = json.loads(dict_str)
    else:
        response = json.loads(judge_context)
    tool_name = response["tool"]["name"]
    return tool_name

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="chat聊天",
            markdown_description="聊天demo：支持多轮对话。支持联网回答用户问题（需要在输入框左边打开联网开关）。默认联网，如不联网在输入框左边关闭联网功能。",
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
            name="项目问答",
            markdown_description="项目级能力demo：支持上传本地zip压缩包项目，支持输入GitHub链接项目，可以进行项目问答和对项目进行修改。",
        ),
    ]

@cl.on_settings_update
async def setup_agent(settings):
    temperature = settings["temperature"]
    top_p = settings["top_p"]
    is_online = settings["is_online"]
    cl.user_session.set("temperature", temperature)
    cl.user_session.set("top_p", top_p)
    cl.user_session.set("is_online", is_online)
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
            Switch(
                id="is_online",
                label="CodeGeeX4 - is_online",
                initial=False
            ),
        ]
    ).send()
    temperature = settings["temperature"]
    top_p = settings["top_p"]
    is_online = settings["is_online"]
    cl.user_session.set("temperature", temperature)
    cl.user_session.set("top_p", top_p)
    cl.user_session.set("is_online", is_online)
    cl.user_session.set("message_history", [])
    chat_profile = cl.user_session.get("chat_profile")
    extract_dir = "repodata"
    if chat_profile == "项目问答":
        res = await cl.AskActionMessage(
            content="请选择项目上传方式",
            actions=[
                cl.Action(name="zip", value="zip", label="本地上传zip文件"),
                cl.Action(name="url", value="url", label="上传GitHub链接"),
            ],
        ).send()
  
        if res.get("value") == "url":
            repo_path =None
            while repo_path == None:
                res = await cl.AskUserMessage(content="请你在下面消息框中提供GitHub仓库URL? ex：https://github.com/THUDM/CodeGeeX2", timeout=3600).send()
                if res:
                    repo_path = clone_repo(res['output'],extract_dir)
                    if repo_path is None:
                        await cl.Message(
                                content=f"您的github链接无法正常下载，请检查项目链接或github网络连通情况。",
                            ).send()
            
            files_list = get_project_files_with_content(repo_path)
            cl.user_session.set("project_index", files_list)
            if len(files_list) > 0:
                await cl.Message(
                    content=f"已成功上传，您可以开始对项目进行提问！",
                ).send()
        elif res.get("value") == "zip":
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


@cl.step(type="tool")
async def bing_search_tool(search_text):
    current_step = cl.context.current_step
    # Simulate a running task
    current_step.input = search_text
    
    prompt_tmp = bing_search_prompt(search_text)
    current_step.output = prompt_tmp

    return prompt_tmp

@cl.on_message
async def main(message: cl.Message):
    chat_profile = cl.user_session.get("chat_profile")
    message_history = cl.user_session.get("message_history")
    
    tool_name = tools_choose_agent(message.content)
    is_online = cl.user_session.get("is_online")

    if chat_profile == "联网聊天":
        if "online_query" in tool_name and is_online:
            prompt_tmp = await bing_search_tool(message.content)
            message_history.append({"role": "tool", "content": prompt_tmp})
        message_history.append({"role": "user", "content": message.content})
        prompt_content = get_cur_base_user_prompt(message_history=message_history)

    elif chat_profile == "项目问答":
        message_history.append({"role": "user", "content": message.content})
        project_index = cl.user_session.get("project_index")
        index_prompt = ""
        index_tmp = """###PATH:{path}\n{code}\n"""
        for index in project_index:
            index_prompt += index_tmp.format(path=index["path"], code=index["content"])
        if len(tool_name)>0:
            prompt_content = get_cur_base_user_prompt(
                    message_history=message_history,
                    index_prompt=index_prompt,
                )
            
        else:
            prompt_content = get_cur_base_user_prompt(message_history=message_history)
        
        
    
    msg = cl.Message(content="")
    await msg.send()
    temperature = cl.user_session.get("temperature")
    top_p = cl.user_session.get("top_p")
    

    if len(prompt_content) / 4 < 120000:
        stream = codegeex4(prompt_content, temperature=temperature, top_p=top_p)

        for part in stream:
            if token := (part or " "):
                await msg.stream_token(token)
    else:
        await msg.stream_token("项目太大了，请换小一点的项目。")

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
