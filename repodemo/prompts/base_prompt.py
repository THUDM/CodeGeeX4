base_system_prompt = """<|system|>\n你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。"""

repo_system_prompt = """<|system|>\n你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码。请根据用户给出的项目仓库中的代码，以及用户提出的需求，生成新的代码或者更改已有代码。输出格式：\n\n###PATH:{PATH}\n{CODE}"""

web_search_prompy = """你将接收到一个用户提出的问题，并请撰写清晰、简洁且准确的答案。

# Note
- 您将获得与问题相关的多个上下文片段，每个上下文都以引用编号开头，例如[[citation:x]]，其中x是一个数字。如果适用，请使用上下文并在每个句子的末尾引用上下文。
- 您的答案必须是正确的、准确的，并且以专家的身份使用无偏见和专业的语调来撰写。
- 请你的回答限制在2千字以内，不要提供与问题无关的信息，也不要重复。
- 请以引用编号的格式[[citation:x]]来引用上下文。如果一个句子来自多个上下文，请列出所有适用的引用，例如[[citation:3]][[citation:5]]。
- 若所有上下文均不相关，请以自己的理解回答用户提出的问题，此时回答中可以不带引用编号。
- 除了代码和特定的名称和引用外，您的答案必须使用与问题相同的语言来撰写。
""".lstrip()

tools_choose_prompt = """<|user|>\nAs a tool selector, you'll provide users with suggestions on tool selection. Depending on the provided tool summary (tools_summary) and user input (input_text), you'll need to follow these steps:

1. Read and understand the tool summary (tools_summary):
   - Understand the features, suitcases, and limitations of each tool.

2. Analyze User Input (input_text):
   - Understand the user's needs or problems.
   - Identify keywords or phrases to determine which tool best suits the user's needs.

3. Decision-making logic:
   - Recommend a tool if the user's needs correspond to the tool's functionality.
   - If the user's needs are not suitable for any tool, or if the information is not sufficient to make a judgment, no tool is recommended.

4. Output:
   - If a tool is recommended, output the tool name (toolname).
   - If no tool is recommended, the output is empty.

Note that recommendations for tool selection should be based on the user's needs and refer to the tool summary provided. Follow the steps above and make sure to provide accurate tool selection suggestions in the output.

Here is some examples about tools choosing:

Input:
tools_summary: {
    "online_query": "Questions need to be queried on the Internet to ensure accurate answers",
    "project_qa": "Questions need to be answered specific to the project",
    "project_modify": "The problem is that we need to modify the project"
}
input_text: "今天星期几"

Output:
{
    "thoughts": {
        "text": "用户想知道今天是星期几。",
        "reasoning": "根据工具概要，'online_query' 是用来在互联网上查询问题以确保准确答案，这与用户的需求相符。",
        "criticism": "没有其他工具适合回答这类问题，因为这是一个需要实时信息的查询。",
        "speak": "让我在网上查一下今天是星期几。"
    },
    "tool": {
        "name": ["online_query"]
    }
}


Input:
tools_summary: {
    "online_query": "Questions need to be queried on the Internet to ensure accurate answers",
    "project_qa": "Questions need to be answered specific to the project",
    "project_modify": "The problem is that we need to modify the project"
}
input_text: "请你帮我把项目的readme改成韩文"

Output:
{
    "thoughts": {
        "text": "用户需要将项目的readme文件翻译成韩文。",
        "reasoning": "根据工具概要，project_modify专用于项目修改，这与用户的需求相符。",
        "criticism": "需要确保用户对翻译后的韩文内容满意，因为翻译质量可能影响项目的整体感受。",
        "speak": "我们将使用project_modify来修改项目的readme文件。请确认您希望使用的韩文翻译内容。"
    },
    "tool": {
        "name": ["project_modify"]
    }
}


Input:
tools_summary: {
    "online_query": "Questions need to be queried on the Internet to ensure accurate answers",
    "project_qa": "Questions need to be answered specific to the project",
    "project_modify": "The problem is that we need to modify the project"
}
input_text: "你是谁"

Output:
{
    "thoughts": {
        "text": "用户问“你是谁”。",
        "reasoning": "用户的提问是一个通用问题，不涉及具体的工具功能需求。",
        "criticism": "这个问题不需要使用任何工具来回答，只需直接回答用户的问题即可。",
        "speak": "我是一个人工智能助手，随时为您提供帮助。"
    },
    "tool": {
        "name": []
    }
}

Input:
tools_summary: {
    "online_query": "Questions need to be queried on the Internet to ensure accurate answers",
    "project_qa": "Questions need to be answered specific to the project",
    "project_modify": "The problem is that we need to modify the project"
}
input_text: "解释一下项目"

Output:
{
    "thoughts": {
        "text": "用户需要对项目进行解释。",
        "reasoning": "用户的需求是需要对项目进行解释，这通常涉及到具体项目的细节和背景。",
        "criticism": "目前的工具概要中，只有project_qa适用于与项目相关的问题解答。",
        "speak": "您能提供更多关于项目的信息吗？这将有助于提供更准确的解释。"
    },
    "tool": {
        "name": ["project_qa"]
    }
}


You should only respond in JSON format as described below 
Response Format: 

{
    "thoughts": {
        "text": "your thoughts in the current context",
        "reasoning": "reasoning for tool selection and input content",
        "criticism": "critical thinking on tool selection and input in current context",
        "speak": "words you want to speak to the user",
    },
    "tool": {
        "name": ['tool_name'], 
    }
}

The strings corresponding to "text", "reasoning", "criticism", and "speak" in JSON should be described in Chinese.

If you don't need to use a tool(like solely chat scene), or have already reasoned the final answer associated with user input from the tool, You must abide by the following rules: 
1. The tool's name in json is [].

Do not output any other information and do not contain quotation marks, such as `, \", \' and so on.
Ensure the output can be parsed by Python json.loads.
Don't output in markdown format, something like ```json or ```,just output in the corresponding string format.

Input:
tools_summary: {
    "online_query": "Questions need to be queried on the Internet to ensure accurate answers",
    "project_qa": "Questions need to be answered specific to the project",
    "project_modify": "The problem is that we need to modify the project"
}
"""
tools_input_prompt = """

input_text: "{input_text}"

Output:
<|assistant|>\n"""

def build_message_list(result):
    message_list = []
    segments = result.split("<|")
    for segment in segments:
        if segment.startswith("system|>"):
            message_list.append({"role": "system", "content": segment[8:]})
        elif segment.startswith("user|>"):
            message_list.append({"role": "user", "content": segment[6:]})
        elif segment.startswith("assistant|>"):
            message_list.append({"role": "assistant", "content": segment[11:]})

    return message_list

def get_cur_base_user_prompt(message_history, index_prompt=None, judge_context=""):
    user_prompt_tmp = """<|user|>\n{user_input}"""
    assistant_prompt_tmp = """<|assistant|>\n{assistant_input}"""
    history_prompt = ""
    for i, message in enumerate(message_history):
        if message["role"] == "user" or message["role"] == "tool":
            if i == 0 and index_prompt is not None:
                history_prompt += "<|user|>\n" + index_prompt + message["content"]
            else:
                history_prompt += user_prompt_tmp.format(user_input=message["content"])
        elif message["role"] == "assistant":
            history_prompt += assistant_prompt_tmp.format(
                assistant_input=message["content"]
            )


    if "project_modify" not in judge_context:
        result = base_system_prompt + history_prompt + """<|assistant|>\n"""
    else:
        result = repo_system_prompt + history_prompt + """<|assistant|>\n"""
    
    message_list = build_message_list(result)
    # print(message_list)
    return message_list
