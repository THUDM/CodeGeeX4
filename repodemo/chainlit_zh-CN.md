![](../resources/logo.jpeg)
## 欢迎使用Chat Demo应用
![](https://github.com/user-attachments/assets/f2cb6c13-a715-4adf-bf3a-b9ca5ee165df)
这是一个简单的演示应用程序，用于展示多轮对话和项目问答功能。


## 功能

- 支持多轮对话
- 支持联网问答
- 支持上传本地zip压缩包项目进行问答和修改
- 支持输入GitHub链接项目进行问答和修改
![](https://github.com/user-attachments/assets/ff6f6e32-457c-4733-815b-b639e4197899)

## 安装

1. 克隆仓库到本地
2. 启动模型，可以通过vllm或者ollama部署模型，提供openai的请求格式，设置部署的api_base和api_key，或者访问[CodeGeeX API](https://open.bigmodel.cn/dev/api#codegeex-4)获取apikey。在.env文件中填写对应的信息
![](https://github.com/user-attachments/assets/6aabc3e4-a930-4853-b511-68b9389fa42f)

```shell
# 使用open.bigmodel.cn API
openai_api_key = ""
openai_api_base = "https://open.bigmodel.cn/api/paas/v4/"
model_name = "codegeex-4"
# 使用vllm
openai_api_key = "EMPTY"
openai_api_base = "http://xxxx:xxxx/v1"
model_name = "codegeex4-all-9b"
```

3. 在.env文件中填写对应模型信息和bing_search_api（如果需要体验联网查询），并且在聊天的时候在输入框左侧打开
联网查询开关，默认关闭。
![](https://github.com/user-attachments/assets/e9d9b620-cfc7-4c2d-bedc-a01d41f79e29)
4. 安装依赖：`pip install -r requirements.txt`
5. 运行应用：`chainlit run run.py --port 8899`

## 注意事项

请确保您的网络环境可以访问CodeGeeX的API。


## 感谢

感谢您使用我们的应用。如果您有任何问题或建议，请随时联系我们。我们期待您的反馈，并致力于为您提供更好的服务。