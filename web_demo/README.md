![](../resources/logo.jpeg)

[English](README.md) | [中文](README_zh.md)

## Online Functionality

CodeGeeX4 supports online search and question answering by calling the Bing API to retrieve search results to access to the latest
information.

## Usage Tutorial

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Bing API Key

Configure `BING_API_KEY` in `backend/apis/bing.py`.

For more details, refer
to [Bing Search API](https://learn.microsoft.com/zh-cn/previous-versions/azure/cognitive-services/Bing-Web-Search/bing-api-comparison)

### 3. Run the Project

```bash
python main.py
>>> Running on local URL:  http://127.0.0.1:8080
```

## Demo

![](resources/demo.png)