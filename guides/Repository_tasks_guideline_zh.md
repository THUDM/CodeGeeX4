
**项目级别使用教程，项目文件增删改，项目问答**

在项目级别任务中，建议使用CodeGeeX4-ALL-9B-128k的模型版本，该模型支持128k的上下文，大约是1万行代码。

出于推理时间成本，以及项目内容仍会超过128k的情况，我们强烈建议在使用CodeGeeX4-ALL-9B-128k模型时，对模型输出进行裁剪。

模型输出裁剪

- bm25&embedding召回
- 超过128k对输入进行截断（这里注意需要保留主题special token，如<|system|>, <|user|>,<|assistant|>等）
- etc.

以下附上一个CodeGeeX4支持的语言列表，您可以使用主要语言做为初步裁剪方式。

主要语言（30种，共支持310中语言）

```
['c', 'c++', 'csharp', 'cuda', 'dart', 'go', 'haskell', 'html', 'java', 'javascript', 'json', 'kotlin', 'lua', 'markdown', 'objective-c++', 'pascal', 'php', 'python', 'r', 'ruby', 'rust', 'scala', 'shell', 'sql', 'swift', 'tex', 'txt', 'typescript', 'vue', 'xml']
```

<a name="heading_0"></a>**项目级别使用教程**

对模型输入进行处理后（128k以内）

我们需要特殊的输入格式激活模型的项目问答和项目文件增删改功能

<a name="heading_1"></a>1. **项目问答**

1. System Prompt

   system prompt这里采用和问答一致的prompt，同样这里我们支持中文和英文两种system prompt。中英文          system prompt不直接影响模型输出的语言，您可以在system prompt的最后使用（请用中文回答。/Please          answer in English.）来诱导模型输出的语言

- 中文system prompt

```
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。（请用中文回答。/Please answer in English.）
```
- English system prompt

```
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly, executable, accurate, and secure, and offer detailed explanations when necessary.（请用中文回答。/Please answer in English.)
```

2. 项目问答输入格式

```
<|system|>
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。<|user|>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
<<用户Query>><|assistant|>\n
```

3. 例子
- 输入

```
<|system|>
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。<|user|>
###PATH: sort.py
def quick_sort(arr):
   if len(arr) <= 1:
      return arr
   needle = "codegeex4-all-9b"
   pivot = arr[len(arr) // 2]
   left = [x for x in arr if x < pivot]
   middle = [x for x in arr if x == pivot]
   right = [x for x in arr if x > pivot]
   return quick_sort(left) + middle + quick_sort(right)
###PATH: calculator.py
def calculate(a, b, op):
   if op == '+':
      return a + b
   elif op == '-':
      return a - b
   elif op == '*':
      return a \* b
   elif op == '/':
      if b == 0:
         return '除数不能为0'
      else:
         return a / b
      else:
         return '无效的运算符'
以上代码中，needle的赋值是什么？<|assistant|>\n
```

- 输出

```
根据以上代码，needle的值是"codegeex4-all-9b"
```

<a name="heading_2"></a>2. **项目文件增删改**

1. System Prompt

   在项目文件增删改这个任务上，需要使用单独的system prompt。同样这里我们支持中文和英文两套system prompt。因为这里的模型输出代码，所以system prompt中不建议加入诱导中英文回答的内容。

- 中文system prompt

```
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码。请根据用户给出的项目仓库中的代码，以及用户提出的需求，生成新的代码或者更改已有代码。输出格式：\n###PATH:{PATH}\n{CODE}
```

- English system prompt

```
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly. Based on the code in the project repository provided by the user and the user's requirements, generate new code or modify existing code. The output format is:\n###PATH: {PATH}\n {CODE}
```

1. 项目问答输入格式

```
<|system|>
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码。请根据用户给出的项目仓库中的代码，以及用户提出的需求，生成新的代码或者更改已有代码。输出格式：\n###PATH:{PATH}\n{CODE}<|user|>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
###PATH: <<File1 Path>>
<<File1 Code Content>>
<<用户Query>><|assistant|>\n
```

2. 例子
- 输入

```
<|system|>
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码。请根据用户给出的项目仓库中的代码，以及用户提出的需求，生成新的代码或者更改已有代码。输出格式：\n###PATH:{PATH}\n{CODE}<|user|>
###PATH: sort.py
def quick_sort(arr):
   if len(arr) <= 1:
      return arr
   needle = "codegeex4-all-9b"
   pivot = arr[len(arr) // 2]
   left = [x for x in arr if x < pivot]
   middle = [x for x in arr if x == pivot]
   right = [x for x in arr if x > pivot]
   return quick_sort(left) + middle + quick_sort(right)
###PATH: calculator.py
def calculate(a, b, op):
   if op == '+':
      return a + b
   elif op == '-':
      return a - b
   elif op == '\*':
      return a \* b
   elif op == '/':
      if b == 0:
         return '除数不能为0'
      else:
         return a / b
   else:
        return '无效的运算符'
写一个新的脚本，为calculator写一个简单测试<|assistant|>\n
```

- 输出

```
###PATH: test_calculator.py
import calculator

def test_calculator():
   assert calculator.calculate(2, 3, '+') == 5
   assert calculator.calculate(5, 2, '-') == 3
   assert calculator.calculate(3, 4, '\*') == 12
   assert calculator.calculate(10, 2, '/') == 5
   assert calculator.calculate(10, 0, '/') == '除数不能为0'
   assert calculator.calculate(10, 2, '%') == '无效的运算符'

test_calculator()
```



