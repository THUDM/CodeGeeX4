![](resources/logo.jpeg)

<p align="center">
    🏠 <a href="https://codegeex.cn" target="_blank">Homepage</a>｜🛠 Extensions <a href="https://marketplace.visualstudio.com/items?itemName=aminer.codegeex" target="_blank">VS Code</a>, <a href="https://plugins.jetbrains.com/plugin/20587-codegeex" target="_blank">Jetbrains</a>｜🤗 <a href="https://huggingface.co/THUDM/codegeex4-all-9b" target="_blank">HF Repo</a> | 🪧 <a href="https://huggingface.co/spaces/THUDM/codegeex-4-9b" target="_blank">HF DEMO</a>
</p>

[English](./README.md) | [中文](./README_zh.md)

# CodeGeeX4: Open Multilingual Code Generation Model

We introduce CodeGeeX4-ALL-9B, the open-source version of the latest CodeGeeX4 model series. It is a multilingual code generation model continually trained on the [GLM-4-9B](https://github.com/THUDM/GLM-4), significantly enhancing its code generation capabilities. Using a single CodeGeeX4-ALL-9B model, it can support comprehensive functions such as code completion and generation, code interpreter, web search, function call, repository-level code Q&A, covering various scenarios of software development. CodeGeeX4-ALL-9B has achieved highly competitive performance  on public benchmarks, such as [BigCodeBench](https://huggingface.co/datasets/bigcode/bigcodebench) and [NaturalCodeBench](https://github.com/THUDM/NaturalCodeBench). It is currently the most powerful code generation model with less than 10B parameters, even surpassing much larger general-purpose models, achieving the best balance in terms of inference speed and model performance.

## Model List

| Model             | Type | Seq Length | Download                                                                                                                                                                                                    |
|-------------------|------|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| codegeex4-all-9b  | Chat | 128K       | [🤗 Huggingface](https://huggingface.co/THUDM/codegeex4-all-9b) [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/codegeex4-all-9b) [🟣 WiseModel](https://wisemodel.cn/models/ZhipuAI/codegeex4-all-9b)    |

## Get Started

Use `4.39.0<=transformers<=4.40.2` to quickly launch [codegeex4-all-9b](https://huggingface.co/THUDM/codegeex4-all-9b)：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("THUDM/codegeex4-all-9b", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "THUDM/codegeex4-all-9b",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).to(device).eval()
inputs = tokenizer.apply_chat_template([{"role": "user", "content": "write a quick sort"}], add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True ).to(device)
with torch.no_grad():
    outputs = model.generate(**inputs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Tutorials
CodeGeeX4-ALL-9B provides three user guides to help users quickly understand and use the model:

1. **[System Prompt Guideline](./guides/System_prompt_guideline.md)**: This guide introduces how to use system prompts in CodeGeeX4-ALL-9B, including the VSCode extension official system prompt, customized system prompts, and some tips for maintaining multi-turn dialogue history.

2. **[Infilling Guideline](./guides/Infilling_guideline.md)**: This guide explains the VSCode extension official infilling format, covering general infilling, cross-file infilling, and generating a new file in a repository.

3. **[repository Tasks Guideline](./guides/Repository_tasks_guideline.md)**: This guide demonstrates how to use repository tasks in CodeGeeX4-ALL-9B, including QA tasks at the repository level and how to trigger the aicommiter capability of CodeGeeX4-ALL-9B to perform deletions, additions, and changes to files at the repository level.

These guides aim to provide a comprehensive understanding and facilitate efficient use of the model.

## Evaluation

CodeGeeX4-ALL-9B is ranked as the most powerful model under 10 billion parameters, even surpassing general models several times its size, achieving the best balance between inference performance and model effectiveness.

CodeGeeX4-ALL-9B scored `48.9` and `40.4` for the `complete` and `instruct` tasks of BigCodeBench, which are the highest scores among models with less than 20 billion parameters. 
![BigCodeBench Test Results](./metric/pics/Bigcodebench.png)
In CRUXEval, a benchmark for testing code reasoning, understanding, and execution capabilities, CodeGeeX4-ALL-9B presented remarkable results with its COT (chain-of-thought) abilities. From easy code generation tasks in HumanEval and MBPP, to very challenging tasks in NaturalCodeBench, CodeGeeX4-ALL-9B also achieved outstanding performance at its scale. It is currently the only code model that supports Function Call capabilities and even achieves a better execution success rate than GPT-4. 
![Function Call Evaluation](./metric/pics/FunctionCall.png)
Furthermore, in the "Code Needle In A Haystack" (NIAH) evaluation, the CodeGeeX4-ALL-9B model demonstrated its ability to retrieve code within contexts up to 128K, achieving a 100% retrieval accuracy in all python scripts.
<p align="center">
  <img src=./metric/pics/NIAH_PYTHON.png alt="图片1描述" width="45%">
  <img src="./metric/pics/NIAH_ALL.png" alt="图片2描述" width="45%">
</p>

Details of the evaluation results can be found in the **[Evaluation](./metric/README.md)**.



## License

The code in this repository is open source under the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) license. The model weights are licensed under the [Model License](MODEL_LICENSE). CodeGeeX4-9B weights are open for academic research. For users who wish to use the models for commercial purposes, please fill in the [registration form](https://open.bigmodel.cn/mla/form).


## Citation

If you find our work helpful, please feel free to cite the following paper:

```
@inproceedings{zheng2023codegeex,
      title={CodeGeeX: A Pre-Trained Model for Code Generation with Multilingual Evaluations on HumanEval-X},
      author={Qinkai Zheng and Xiao Xia and Xu Zou and Yuxiao Dong and Shan Wang and Yufei Xue and Zihan Wang and Lei Shen and Andi Wang and Yang Li and Teng Su and Zhilin Yang and Jie Tang},
      booktitle={KDD},
      year={2023}
}
```
