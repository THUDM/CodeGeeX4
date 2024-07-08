# CodeGeeX

#   欢迎使用我的chat dome应用

这是一个简单的演示应用程序。

## 使用说明

1. 输入您的问题
2. 等待回复
3. 享受对话！

## 功能

-  支持多轮对话
-  支持联网问答
-  支持上传本地zip压缩包项目，可以进行项目问答和对项目进行修改

## 安装

1. 克隆仓库到本地
2. 设置模型，可以选择本地模型或者api模型,如果使用本地模型需要到run_local.py里设置local_model_path
3. 如果要用联网问答需要设置bingsearch API，在utils/bingsearch.py中设置bingsearch_api_key
3. 安装依赖：`pip install -r requirements.txt`
4. 运行应用：`chainlit run run.py --port 8888` 如果用本地：`chainlit run run_local.py --port 8888`


## 注意

请确保您的网络环境可以访问CodeGeeX的API。

##   免责声明

本应用仅供学习和研究使用，不得用于任何商业用途。开发者不对因使用本应用而导致的任何损失或损害负责。

##     感谢

感谢您使用我们的应用。如果您有任何问题或建议，请随时联系我们。我们期待您的反馈，并致力于为您提供更好的服务。
