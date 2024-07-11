![](../resources/logo.jpeg)

[English](README.md) | [中文](README_zh.md)

## 本地模式

CodeGeeX新版插件**支持离线模式**，可使用离线部署的模型完成自动补全以及简单对话功能。

## 使用教程

### 1. 安装依赖项

```bash
cd local_mode
pip install -r requirements.txt
```

### 2. 运行项目

```bash
python main.py --model_name_or_path THUDM/codegeex4-all-9b --device cuda --bf16 true

>>> Running on local URL:  http://127.0.0.1:8080
```

### 3. 设置api地址和模型名称

如下图所示，打开插件后进入本地模式，在设置中输入api地址和模型名称。
![](resources/pic1.png)

### 4. 开始使用

点击‘连接’进行测试，或点击‘Ask CodeGeeX’即可开始使用。

## Demo

![](resources/demo_zh.gif)