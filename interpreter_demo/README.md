# Codegeex4 Interpreter Gradio

Fully local gradio demo of CodeGeeX4 Interpreter.

## Usage

### Install Dependencies

```python
pip install gradio requests
```

### Build & Launch Sandbox

```bash
docker build -t sandbox -f Dockerfile.sandbox .
docker run --name sandbox --publish 8080:8080 sandbox
```

### Launch Demo

```bash
python app.py --tgi-addr <tgi-addr>
```

## Docs

Check out the [documentation](./SANDBOX.md) for the sandbox API.
