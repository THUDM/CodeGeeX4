**Project-Level Usage Tutorial: Project File Add, Delete, Modify, Project Q&A**

For project-level tasks, it is recommended to use the CodeGeeX4-ALL-9B-128k model version. This model supports 128k context, which is approximately 10,000 lines of code.

Due to the inference time cost and the possibility of project content exceeding 128k, we strongly recommend trimming the model output when using the CodeGeeX4-ALL-9B-128k model.

**Model Output Trimming**

- BM25 & embedding recall
- Truncate input exceeding 128k (make sure to retain theme special tokens, such as [CLS], [SEP], etc.)
- Etc.

Below is a list of languages supported by CodeGeeX4. You can use the primary languages as an initial way to trim the output.

**Primary Languages (30 out of 310 languages supported)**

```
['c', 'c++', 'csharp', 'cuda', 'dart', 'go', 'haskell', 'html', 'java', 'javascript', 'json', 'kotlin', 'lua', 'markdown', 'objective-c++', 'pascal', 'php', 'python', 'r', 'ruby', 'rust', 'scala', 'shell', 'sql', 'swift', 'tex', 'txt', 'typescript', 'vue', 'xml']
```

<a name="heading_0"></a>**Repository-Level Task Tutorial**

After processing the model input (within 128k),

we need a special input format to activate the model's project Q&A and project file add, delete, and modify functions.

<a name="heading_1"></a>1. **Repository Q&A**

1. **System Prompt**

   The system prompt here uses the same prompt as Q&A. We support both Chinese and English system prompts. The system prompt language does not directly affect the model's output language. You can use phrases like "请用中文回答。" or "Please answer in English." at the end of the system prompt to induce the model's output language.
- 中文system prompt

```
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码，并在必要时提供详细的解释。（请用中文回答。/Please answer in English.）
```
- English system prompt

```
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly, executable, accurate, and secure, and offer detailed explanations when necessary.（请用中文回答。/Please answer in English.)
```

2. Repository Q&A Format

```
<|system|>
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly, executable, accurate, and secure, and offer detailed explanations when necessary.<|user|>
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
<<Query>><|assistant|>\n
```

3. Example：
- Prompt

```
<|system|>
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly, executable, accurate, and secure, and offer detailed explanations when necessary.<|user|>
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
         return 'devider can not be 0'
      else:
         return a / b
      else:
         return 'error'
what's the needle value in above code snipptss<|assistant|>\n
```

- output

```
Acoording to the above code snippet, the needle value is "codegeex4-all-9b".
```

<a name="heading_2"></a>2. **Repository File Add, Delete, Modify**

1. **System Prompt**

   For the task of adding, deleting, and modifying project files, a separate system prompt is needed. Similarly, we support both Chinese and English system prompts here. Since the model's output is code, it is not recommended to include content that induces responses in Chinese or English in the system prompt.

- 中文system prompt

```
你是一位智能编程助手，你叫CodeGeeX。你会为用户回答关于编程、代码、计算机方面的任何问题，并提供格式规范、可以执行、准确安全的代码。请根据用户给出的项目仓库中的代码，以及用户提出的需求，生成新的代码或者更改已有代码。输出格式：\n###PATH:{PATH}\n{CODE}
```

- English system prompt

```
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly. Based on the code in the project repository provided by the user and the user's requirements, generate new code or modify existing code. The output format is:\n###PATH: {PATH}\n {CODE}
```

1. Repository File Add, Delete, Modify Format

```
<|system|>
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly. Based on the code in the project repository provided by the user and the user's requirements, generate new code or modify existing code. The output format is:\n###PATH: {PATH}\n {CODE}<|user|>
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
<<Query>><|assistant|>\n
```

2. Example:
- Prompt

```
<|system|>
You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly. Based on the code in the project repository provided by the user and the user's requirements, generate new code or modify existing code. The output format is:\n###PATH: {PATH}\n {CODE}<|user|>
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
         return 'devider can not be 0'
      else:
         return a / b
      else:
         return 'error'
Write a new script for calculator to write a simple test|assistant|>\n
```

- Output

```
###PATH: test_calculator.py
import calculator

def test_calculator():
   assert calculator.calculate(2, 3, '+') == 5
   assert calculator.calculate(5, 2, '-') == 3
   assert calculator.calculate(3, 4, '\*') == 12
   assert calculator.calculate(10, 2, '/') == 5
   assert calculator.calculate(10, 0, '/') == 'devider can not be 0'
   assert calculator.calculate(10, 2, '%') == 'error'

test_calculator()
```



