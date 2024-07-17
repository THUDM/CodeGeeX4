![](../resources/logo.jpeg)

[English](README.md) | [中文](README_zh.md)

## Function Call

CodeGeeX4代模型支持Function Call，可根据问题，在候选集中选择**一个**或**多个**工具进行调用。

## 使用示例

### 1. 安装依赖项

```bash
cd function_call_demo
pip install -r requirements.txt
```

### 2. 运行脚本

```bash
python main.py
>>> [{"name": "weather", "arguments": {"location": "Beijing"}}]
```

## 说明

### 1.多工具单次调用

示例脚本中，只提供了唯一工具作为候选。但在实际使用时，可根据需要提供多个工具作为候选，例如：

```python
tool_content = {
    "function": [
        {
            "name": "weather",
            "description": "Use for searching weather at a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "description": "the location need to check the weather",
                        "type": "str",
                    }
                },
                "required": [
                    "location"
                ]
            }
        },
        {
            "name": "Cooking/queryDish",
            "description": "Cooking API, providing cooking methods for different cuisines. It queries dish information based on specified parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuisine": {
                        "description": "Specify the cuisine to be queried, such as Sichuan cuisine, Cantonese cuisine, Hunan cuisine."
                    },
                    "dish": {
                        "description": "Specify the name of the dish to be queried."
                    },
                    "difficulty": {
                        "description": "Specify the difficulty of the dish to be queried, such as beginner, intermediate, advanced."
                    }
                },
                "required": [
                    "cuisine"
                ]
            }
        }
    ]
}
response, _ = model.chat(
    tokenizer,
    query="How to make Kung-Pao Chicken",
    history=[{"role": "tool", "content": tool_content}],
    max_new_tokens=1024,
    temperature=0.1
)
```

得到以下结果

```text
[{'name': 'Cooking/queryDish', 'arguments': {'cuisine': 'Sichuan cuisine', 'dish': 'Kung-Pao Chicken'}}]
```

### 2.多工具多次调用

此外，针对复杂问题，模型具备在候选工具中选择多个工具进行调用的能力，例如：

```python
tool_content = {
    "function": [
        {
            "name": "flight_book",
            "description": "Book a flight for a specific route and airlines",
            "parameters": {
                "type": "dict",
                "properties": {
                    "from": {
                        "type": "string",
                        "description": "The departure city in full name."
                    },
                    "to": {
                        "type": "string",
                        "description": "The arrival city in full name."
                    },
                    "airlines": {
                        "type": "string",
                        "description": "The preferred airline."
                    }
                },
                "required": [
                    "from",
                    "to",
                    "airlines"
                ]
            }
        },
        {
            "name": "hotel_book",
            "description": "Book a hotel for a specific location for the number of nights",
            "parameters": {
                "type": "dict",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city where the hotel is located."
                    },
                    "nights": {
                        "type": "integer",
                        "description": "Number of nights for the stay."
                    }
                },
                "required": [
                    "location",
                    "nights"
                ]
            }
        }
    ]
}
response, _ = model.chat(
    tokenizer,
    query="Book a flight from Seattle to Boston with American Airlines and book a hotel in Boston for 4 nights.",
    history=[{"role": "tool", "content": tool_content}],
    max_new_tokens=1024,
    temperature=0.1
)
```

得到以下结果

```text
[{'name': 'flight_book', 'arguments': {'from': 'Seattle', 'to': 'Boston', 'airlines': 'American Airlines'}}, {'name': 'hotel_book', 'arguments': {'location': 'Boston', 'nights': 4}}]
```

