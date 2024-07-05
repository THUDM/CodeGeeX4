base_system_prompt = """<|system|>\n你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。"""

repo_system_prompt = """<|system|>\n你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码。请根据用户给出的项目仓库中的代码，以及用户提出的需求，生成新的代码或者更改已有代码。输出格式：\n\n###PATH:{PATH}\n{CODE}"""

judge_task_prompt = """<|system|>\n你是一位任务分类专家，请你对用户的输入进行分类（问答/修改/正常），如果用户的输入是对项目进行提问则只需要输出问答两个字，如果用户的输入是对项目进行修改或增加则只需要输出修改两个字，如果用户输入的是一个与项目无关的问题则只需要输出正常两个字。<|user|>\n{user_input}<|assistant|>\n"""

web_judge_task_prompt ="""<|system|>\n你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。<|user|>\n{user_input}\n这个问题需要进行联网来回答吗？仅回答“是”或者“否”。<|assistant|>\n"""

# judge_task_prompt = """<|system|>\n你是一位任务分类专家，请你对用户的输入进行分类（问答/修改），如果用户的输入是对项目进行提问则只需要输出问答两个字，如果用户的输入是对项目进行修改或增加则只需要输出修改两个字。<|user|>\n{user_input}<|assistant|>\n"""
web_search_prompy = """
你将接收到一个用户提出的问题，并请撰写清晰、简洁且准确的答案。

# Note
- 您将获得与问题相关的多个上下文片段，每个上下文都以引用编号开头，例如[[citation:x]]，其中x是一个数字。如果适用，请使用上下文并在每个句子的末尾引用上下文。
- 您的答案必须是正确的、准确的，并且以专家的身份使用无偏见和专业的语调来撰写。
- 请你的回答限制在2千字以内，不要提供与问题无关的信息，也不要重复。
- 请以引用编号的格式[[citation:x]]来引用上下文。如果一个句子来自多个上下文，请列出所有适用的引用，例如[[citation:3]][[citation:5]]。
- 若所有上下文均不相关，请以自己的理解回答用户提出的问题，此时回答中可以不带引用编号。
- 除了代码和特定的名称和引用外，您的答案必须使用与问题相同的语言来撰写。
""".lstrip()

def get_cur_base_user_prompt(message_history,index_prompt = None,judge_context = ""):
    user_prompt_tmp = """<|user|>\n{user_input}"""
    assistant_prompt_tmp = """<|assistant|>\n{assistant_input}"""
    history_prompt = ""
    for i,message in enumerate(message_history):
        if message['role'] == 'user':
            if i==0 and index_prompt is not None:
                history_prompt += "<|user|>\n"+index_prompt+message['content']
            else:
                history_prompt += user_prompt_tmp.format(user_input=message['content'])
        elif message['role'] ==  'assistant':
            history_prompt += assistant_prompt_tmp.format(assistant_input=message['content'])
   
    # print("修改" not in judge_context)
    # print(judge_context)
    if "修改" not in judge_context:
        result = base_system_prompt+history_prompt+"""<|assistant|>\n"""
    else:
        result = repo_system_prompt+history_prompt+"""<|assistant|>\n"""
    print(result)
    return result