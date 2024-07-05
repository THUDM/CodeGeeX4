
**Code Completion Tutorial: Contextual, Cross-File, and Project-Level Completion**

This tutorial primarily introduces the code completion capabilities of plugin-enabled models. These capabilities include contextual completion, cross-file completion, and project-level file completion.

- **Contextual Completion:** Within the same code file, based on the cursor's position and the surrounding context.
- **Cross-File Completion:** Enhances code completion capabilities by incorporating dependencies or related files of the current code file.
- **Project-Level Completion:** The model can generate complete new files based on your project information and requirements.

  You can use the CodeGeeX4-ALL-9B-128k model and control memory requirements by setting different `max_length` values. For example, you can set `max_length` to 16k or 32k to run the model on consumer-grade graphics cards.

<a name="heading_0"></a>**Code Completion Usage Tutorial**

<a name="heading_1"></a>1. **Contextual Completion**

1. **File Path:** `"###PATH:"` + relative file path or file name
2. **Language Tag:** This is very important and must be included. The list of languages is mentioned above, and the format generally starts with the language's initial capital letter, with a few exceptions. If unsure about the language, you can leave it blank after the colon. All language tags start with `"###LANGUAGE:"`.
3. **Two Modes:** `"###MODE:"`, `LINE` generates a single line, and `BLOCK` generates multiple lines. The default is `BLOCK` mode.
4. **Format:**
```
<|user|>
###PATH:{path}
###LANGUAGE:{code_language}
###MODE:{LINE/BLOCK}
<|code_suffix|>{code}<|code_prefix|>{code}<|code_middle|><|assistant|>\n
```
5. Example:
When all information including path, code_language, mode, suffix, and prefix is provided:

```
<|user|>
###PATH:src.py
###LANGUAGE:Python
###MODE:LINE/BLOCK
<|code_suffix|>            else:
                depth -= 1

        return max_depth

    return [parse_paren_group(x) for x in paren_string.split(' ') if x]
<|code_prefix|>from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
   [2, 3, 1, 3]
"""
<|code_middle|><|assistant|>\n
```

- Situation with no language and no suffix provided

```
<|user|>
###PATH:src.py
###LANGUAGE:
###MODE:LINE/BLOCK
<|code_suffix|><|code_prefix|>from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
   """
<|code_middle|><|assistant|>\n
```

<a name="heading_2"></a>2. **Cross File Infilling**

1. Please format reference code as below:

```
###REFERENCE:
###PATH: relative file path or file name
code snippet
###REFERENCE:
###PATH: relative file path or file name
code snippet
```

2. **File Path:** `"###PATH:"` + relative file path or file name
3. **Language Tag:** This is very important and must be included. The list of languages is mentioned above, and the format generally starts with the language's initial capital letter, with a few exceptions. If unsure about the language, you can leave it blank after the colon. All language tags start with `"###LANGUAGE:"`.
4. **Two Modes:** `"###MODE:"`, `LINE` generates a single line, and `BLOCK` generates multiple lines. The default is `BLOCK` mode.
5. **Format:**
```
<|user|>
###REFERENCE:
###PATH:{path}
{code}
...
...
...
###REFERENCE:
###PATH:{path}
{code}
###PATH:{path}\n\n###LANGUAGE:{code_language}\n###MODE:{LINE/BLOCK}\n<|code_suffix|>{code}<|code_prefix|>{code}<|code_middle|><|assistant|>\n
```
6. Example:
```
|Python
<|user|>
###PATH:./sort/quick_sort.py
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

arr = [3,6,8,10,1,2,1]
print(quick_sort(arr))
###PATH:src.py
###LANGUAGE:Python
###MODE:LINE/BLOCK
<|code_suffix|>            else:
                depth -= 1

        return max_depth

    return [parse_paren_group(x) for x in paren_string.split(' ') if x]
<|code_prefix|>from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
<|code_middle|><|assistant|>\n
```

<a name="heading_3"></a>3. **Repository Level File Generation**

1. You can use the project-level add, delete, and modify format to complete the task of adding a file in the project.
2. Related files: Example format is as follows:

```
###REFERENCE:
###PATH: relative file path or file name
代码
###REFERENCE:
###PATH: relative file path or file name
代码
```

3. **File Path:** `"###PATH:"` + relative file path or file name
4. **Language Tag:** This is very important and must be included. The list of languages is mentioned above, and the format generally starts with the language's initial capital letter, with a few exceptions. If unsure about the language, you can leave it blank after the colon. All language tags start with `"###LANGUAGE:"`.
5. **Two Modes:** `"###MODE:"`, `LINE` generates a single line, and `BLOCK` generates multiple lines. The default is `BLOCK` mode.
6. **Format:**
```
<|user|>
###REFERENCE:
###PATH:{path}
{code}
...
...
...
###REFERENCE:
###PATH:{path}
{code}
###PATH:{path}
###LANGUAGE:{code_language}
###MODE:{LINE/BLOCK}
<|code_suffix|>{code}<|code_prefix|>{code}<|code_middle|><|assistant|>\n
```
7. Example:

```
<|user|>
###PATH:./sort/quick_sort.py
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

arr = [3,6,8,10,1,2,1]
print(quick_sort(arr))
###PATH:src.py
###LANGUAGE:Python
###MODE:LINE/BLOCK
<|code_suffix|>            else:
                depth -= 1

        return max_depth

    return [parse_paren_group(x) for x in paren_string.split(' ') if x]
<|code_prefix|>from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
<|code_middle|><|assistant|>\n
```


