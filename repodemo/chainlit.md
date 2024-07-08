# CodeGeeX

## Welcome to My Chat Dome Application

This is a simple demonstration application.

## Instructions

1. Enter your question
2. Wait for a reply
3. Enjoy the conversation!

## Features

- Supports multi-turn conversations
- Supports internet-connected Q&A
- Allows uploading local zip project files for project-related Q&A and modifications

## Installation

1. Clone the repository to your local machine
2. Set up the model; you can choose between a local model or an API model. If using a local model, set `local_model_path` in `run_local.py`
3. For internet-connected Q&A, set the Bing Search API key in `utils/bingsearch.py` (`bingsearch_api_key`)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `chainlit run run.py --port 8888`. For local use: `chainlit run run_local.py --port 8888`

## Notes

Ensure that your network environment can access the CodeGeeX API.

## Disclaimer

This application is for educational and research purposes only. It must not be used for any commercial purposes. The developer is not responsible for any loss or damage caused by the use of this application.

## Acknowledgements

Thank you for using our application. If you have any questions or suggestions, please feel free to contact us. We look forward to your feedback and are committed to providing better service.