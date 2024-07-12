# CodeGeeX

# Welcome to My Chat Demo Application

This is a simple demonstration application.

## Instructions

1. Enter your question.
2. Wait for a response.
3. Enjoy the conversation!

## Features

- Supports multi-turn conversations.
- Supports online Q&A.
- Supports uploading local zip packages for project Q&A and modifications.
- Supports inputting GitHub project links for project Q&A and modifications.

## Installation

1. Clone the repository locally.
2. Start the model. You can deploy the model using vllm or ollama, provide the OpenAI request format, and set the deployed `api_base` and `api_key`. Alternatively, visit [CodeGeeX API](https://open.bigmodel.cn/dev/api#codegeex-4) to get the API key.

```shell
#use open.bigmodel.cn api
openai_api_key = "<|apikey|>"
openai_api_base = "https://open.bigmodel.cn/api/paas/v4/"
model_name = "codegeex-4"
#use vllm
openai_api_key = "EMPTY"
openai_api_base = "http://xxxx:xxxx/v1"
model_name = "codegeex4-all-9b"
```

3. Fill in the corresponding model information and `bing_search_api` (if you want to experience online search) in the `.env` file.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the application: `chainlit run run.py --port 8899`.

## Note

Please ensure your network environment can access the CodeGeeX API.

## Disclaimer

This application is for educational and research purposes only and should not be used for any commercial purposes. The developer is not responsible for any loss or damage caused by the use of this application.

## Acknowledgements

Thank you for using our application. If you have any questions or suggestions, please feel free to contact us. We look forward to your feedback and are committed to providing you with better service.