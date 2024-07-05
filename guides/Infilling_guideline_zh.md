
**代码补全使用教程，上下文补全，跨文件补全，项目级别补全**

本篇教程中，主要介绍了插件功能的模型的代码补全能力。代码补全能力包括上下文补全，跨文件补全和项目级文件补全。

- 上下文补全：在同一个代码文件内，根据光标所在位置，上下文信息。
- 跨文件补全：引入当前代码文件的依赖文件或者相关文件，增强代码补全的能力。
- 项目级别补全：模型可以根据您的项目信息，以及您的需求，为您生成完整的新文件。

  您可以使用CodeGeeX4-ALL-9B-128k模型，通过设置不同的max_length控制对显存的需求。例如，您可以将max_length设置在16k或者32k以便将模型跑在消费级显卡上

<a name="heading_0"></a>**代码补全使用教程**

<a name="heading_1"></a>1. **上下文填空**

1. 文件路径："###PATH:" + 文件相对路径或文件名
2. 语言标签非常重要，必须要加上，语言列表见上方，格式一般是语言开头大写，有个别特殊；在不确定语言的情况下，冒号后面可以空着），所有语言标签都是以"###LANGUAGE:"开头，不作另外区分。
3. 两个种模式："###MODE:"，LINE生成单行，BLOCK生成多行。默认BLOCK模式。
4. 格式：
```
<|user|>
###PATH:{path}
###LANGUAGE:{code_language}
###MODE:{LINE/BLOCK}
<|code_suffix|>{code}<|code_prefix|>{code}<|code_middle|><|assistant|>\n
```
5. 示例如下:
- 有path,code_language,mode,suffix,prefix全部信息的情况

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

- 没有语言、没有后缀的情况

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

<a name="heading_2"></a>2. **跨文件补全**

1. 相关文件：格式示例如下

```
###REFERENCE:
###PATH: 文件相对路径或文件名
代码
###REFERENCE:
###PATH: 文件相对路径或文件名
代码
```

2. 文件路径："###PATH:" + 文件相对路径或文件名
3. 语言标签非常重要，必须要加上，语言列表见上方，格式一般是语言开头大写，有个别特殊；在不确定语言的情况下，冒号后面可以空着），所有语言标签都是以"###LANGUAGE:"开头，不作另外区分。
4. 两个种模式："###MODE:"，LINE生成单行，BLOCK生成多行。默认BLOCK模式。
5. 格式：
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
###PATH:{path}\n\n###LANGUAGE:{code_language}\n###MODE:{LINE/BLOCK}\n<|code_suffix|>{code}<|code_prefix|>{code}<|code_middle|><|assistant|>
6. 示例如下:

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

<a name="heading_3"></a>3. **项目级文件补全**

1. 您可以使用项目级增删改的格式，完成在项目中补一个文件的任务
2. 相关文件：格式示例如下

```
###REFERENCE:
###PATH: 文件相对路径或文件名
代码
###REFERENCE:
###PATH: 文件相对路径或文件名
代码
```

3. 文件路径："###PATH:" + 文件相对路径或文件名
4. 语言标签非常重要，必须要加上，语言列表见上方，格式一般是语言开头大写，有个别特殊；在不确定语言的情况下，冒号后面可以空着），所有语言标签都是以"###LANGUAGE:"开头，不作另外区分。
5. 两个种模式："###MODE:"，LINE生成单行，BLOCK生成多行。默认BLOCK模式。
6. 格式：
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
7. 示例如下:

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


