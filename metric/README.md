# The Most Powerful Versatile Code Model Under 10 Billion Parameters

CodeGeeX4-ALL-9B, the open-source version of the latest generation of the CodeGeeX4 series, iterates on the powerful language capabilities of GLM4, significantly enhancing code generation capabilities. Using a single CodeGeeX4-ALL-9B model, it supports comprehensive functionalities such as code completion and generation, code interpreter, online search, tool invocation, repository-level long code Q&A and generation, covering various programming and development scenarios. CodeGeeX4-ALL-9B has achieved highly competitive performance on multiple authoritative code capability evaluation sets, such as NaturalCodeBench and BigCodeBench. It is the most powerful model under 10 billion parameters, even surpassing general models several times its size, achieving the best balance between inference performance and model effectiveness.

## 1. BigCodeBench

BigCodeBench test results show that CodeGeeX4-ALL-9B performs the best at the same size:

![BigCodeBench Test Results](./pics/Bigcodebench.png)

## 2. NaturalCodeBench & HumanEval
NaturalCodeBench test results show that CodeGeeX4-ALL-9B achieves the best results in tasks such as code completion, code interpreter, code Q&A, code translation, and code repair:

![NaturalCodeBench Test Results](./pics/NCB&HUMANEVAL.png)

## 3. Code Needle In A Haystack

CodeGeeX4-ALL-9B's context handling capability has reached 128K, an 8-fold increase compared to the previous generation model!

For code large models under 10B parameters, accurately extracting information from massive amounts of code is a key challenge. CodeGeeX4-ALL-9B's upgraded support for 128K context enables it to process and utilize longer code files, and even information from project code, helping the model to understand complex and detail-rich code more deeply. Based on the longer context, CodeGeeX4-ALL-9B can handle more complex project-level tasks, accurately answering content from different code files and making modifications to the code even when the input length increases significantly.

In the "Needle In A Haystack" (NIAH) evaluation, the CodeGeeX4-ALL-9B model demonstrated its ability to embed and retrieve code within contexts up to 128K, achieving a 100% retrieval accuracy.

![NIAH_PYTHON Evaluation](./pics/NIAH_PYTHON.png)

![NIAH_ALL_FILES Evaluation](./pics/NIAH_ALL.png)

The above figures show the test results in a test set composed entirely of Python code, where an assignment statement such as `zhipu_codemodel = "codegeex"` (Needle) is inserted, and the model is tested on whether it can correctly answer the value of `zhipu_codemodel`. CodeGeeX4-All-9B completed the task 100%.

## 4. Function Call Capabilities

CodeGeeX4-ALL-9B is currently the only code large model that implements Function Call capabilities.

The Berkeley Function Calling Leaderboard is the first test set that can comprehensively evaluate the function calling capabilities of large models. The AST dataset evaluates the model's calling capabilities for Java, JavaScript, and Python programs; the Executable dataset evaluates the model's function calling capabilities for real-world API scenarios.

![Berkeley Function Calling Leaderboard](./pics/FunctionCall.png)

CodeGeeX4-ALL-9B underwent comprehensive testing on the Berkeley Function Calling Leaderboard, including various forms of function calls, different function call scenarios, and function call executability tests, achieving the following results: a call success rate of over 90% in both AST and Exec test sets.

## 5. Cross-File Completion

Cross-File Evaluation is a multilingual benchmark built on diverse real-world repositories in Python, Java, TypeScript, and C#. It uses a static-analysis-based method to strictly require cross-file context for accurate code completion.

| Model            | PYTHON EM | PYTHON ES | JAVA EM | JAVA ES | TypeScript EM | TypeScript ES | C# EM  | C# ES  |
|------------------|------------|------------|----------|----------|----------------|----------------|---------|---------|
| DeepSeekCoder-7B | 29.9       | 62.9       | 39.8     | 74.8     | 39             | 77             | 52.2    | 78.1    |
| StarCoder2-7B    | 25.3       | 58         | 31.4     | 67.4     | 33.3           | 73.2           | 43.5    | 69.8    |
| CodeLlama-7B     | 23.5       | 53.5       | 33.9     | 68.4     | 11.5           | 71.5           | 50.6    | 75.4    |
| CodeGeeX-9B      | 32.3      | 70.3      | 48.6    | 84.4    | 35.3          | 78.0          | 48.0   | 84.8   |
