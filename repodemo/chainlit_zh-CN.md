# CodeGeeX

# 欢迎使用我的chat demo应用

这是一个简单的演示应用程序。

## 使用说明

1. 输入您的问题
2. 等待回复
3. 享受对话！

## 功能

-  支持多轮对话
-  支持联网问答
-  支持上传本地zip压缩包项目，可以进行项目问答和对项目进行修改
-  支持输入GitHub链接项目，可以进行项目问答和对项目进行修改。

## 安装

1. 克隆仓库到本地
2. 启动模型，可以通过vllm或者ollama部署模型，提供openai的请求格式，设置部署的api_base和api_key，或者访问[CodeGeeX API](https://open.bigmodel.cn/dev/api#codegeex-4)获取apikey.

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

3. 到.env文件里填写对应模型信息和bing_search_api(如果需要体验联网查询)
4. 安装依赖：`pip install -r requirements.txt`
5. 运行应用：`chainlit run run.py --port 8899` 


## 注意

请确保您的网络环境可以访问CodeGeeX的API。

## 免责声明

本应用仅供学习和研究使用，不得用于任何商业用途。开发者不对因使用本应用而导致的任何损失或损害负责。

## 感谢

感谢您使用我们的应用。如果您有任何问题或建议，请随时联系我们。我们期待您的反馈，并致力于为您提供更好的服务。
