# Codegeex4 代码解释器DEMO

完全本地可运行的 CodeGeeX4 代码解释器.

## 使用方法

### 安装依赖

```python
pip install gradio requests
```

### 构建并启动本地沙盒环境

```bash
docker build -t sandbox -f Dockerfile.sandbox .
docker run --name sandbox --publish 8080:8080 sandbox
```

### 启动DEMO

```bash
python app.py --tgi-addr <tgi-addr>
```

## 文档

参考 [沙盒API文档](./SANDBOX.md)。
