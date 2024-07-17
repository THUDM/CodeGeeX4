![](../resources/logo.jpeg)

[English](README.md) | [Chinese](README_zh.md)

## Function Call

The CodeGeeX4 model supports 'Function Call', which allows model to select **one** or **multiple** tools from the candidates based on
the problem.

## Usage Example

### 1. Install Dependencies

```bash
cd function_call_demo
pip install -r requirements.txt
```

### 2. Run the Script

```bash
python main.py
>>> [{"name": "weather", "arguments": {"location": "Beijing"}}]
```

## Explanation

### 1. Single Call of Multiple Tools

In the example script, only one tool is provided as a candidate. However, you can also provide multiple tools as candidates as needed.
Here is an example:

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

The following result is obtained

```text
[{'name': 'Cooking/queryDish', 'arguments': {'cuisine': 'Sichuan cuisine', 'dish': 'Kung-Pao Chicken'}}]
```

### 2. Multiple Invocations of Multiple Tools

Additionally, for complex problems, the model has the ability to select and call multiple tools from the candidates. Here is an example:

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

The following result is obtained

```text
[{'name': 'flight_book', 'arguments': {'from': 'Seattle', 'to': 'Boston', 'airlines': 'American Airlines'}}, {'name': 'hotel_book', 'arguments': {'location': 'Boston', 'nights': 4}}]
```
