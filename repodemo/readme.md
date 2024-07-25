![](../resources/logo.jpeg)
[English](./readme.md) | [中文](./readme_zh.md)
## Welcome to Chat Demo Application
![](https://github.com/user-attachments/assets/f2cb6c13-a715-4adf-bf3a-b9ca5ee165df)
This is a simple demo application designed to showcase multi-turn conversations and project Q&A functionalities.

## Features

- Supports multi-turn conversations
- Supports online Q&A
- Supports uploading local zip files for project Q&A and modifications
- Supports inputting GitHub project links for Q&A and modifications
![](https://github.com/user-attachments/assets/ff6f6e32-457c-4733-815b-b639e4197899)
## Installation

1. Clone the repository locally.
2. Start the model. You can deploy the model via vllm or ollama, provide the OpenAI request format, set the deployed `api_base` and `api_key`, or access the [CodeGeeX API](https://open.bigmodel.cn/dev/api#codegeex-4) to get an API key. Fill in the corresponding information in the .env file.
![](https://github.com/user-attachments/assets/6aabc3e4-a930-4853-b511-68b9389fa42f)

```shell
# Using open.bigmodel.cn API
openai_api_key = ""
openai_api_base = "https://open.bigmodel.cn/api/paas/v4/"
model_name = "codegeex-4"
# Using vllm
openai_api_key = "EMPTY"
openai_api_base = "http://xxxx:xxxx/v1"
model_name = "codegeex4-all-9b"
```

3. Fill in the corresponding model information and `bing_search_api` (if you want to experience online queries) in the .env file. Turn on the online query switch on the left side of the input box during the chat, which is off by default.
![](https://github.com/user-attachments/assets/e9d9b620-cfc7-4c2d-bedc-a01d41f79e29)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `chainlit run run.py --port 8899`

## Notes

Please ensure your network environment can access the CodeGeeX API.

## Acknowledgments

Thank you for using our application. If you have any questions or suggestions, please feel free to contact us. We look forward to your feedback and are committed to providing you with better service.