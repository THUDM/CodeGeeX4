import zipfile
import os
import json


def unzip_file(zip_path, extract_dir):
    """
    解压zip文件到指定目录，并在指定目录下创建一个新的目录存放解压后的文件

    参数:
    zip_path (str): zip压缩包的地址
    extract_dir (str): 指定解压的目录

    返回:
    str: 解压后的路径
    """
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    base_name = os.path.basename(zip_path)
    dir_name = os.path.splitext(base_name)[0]
    new_extract_dir = os.path.join(extract_dir, dir_name)

    if not os.path.exists(new_extract_dir):
        os.makedirs(new_extract_dir)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(new_extract_dir)

    return new_extract_dir


def get_project_files_with_content(project_dir):
    """
    获取项目目录下所有文件的相对路径和内容

    参数:
    project_dir (str): 项目目录地址

    返回:
    list: 包含字典的列表，每个字典包含文件的相对路径和内容
    """
    files_list = []

    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if filter_data(file):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_dir)
                if "__MACOSX" in relative_path:
                    continue
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                files_list.append({"path": relative_path, "content": content})
            else:
                continue

    return files_list


def filter_data(obj):
    LANGUAGE_TAG = {
        "c++": "// C++",
        "cpp": "// C++",
        "c": "// C",
        "c#": "// C#",
        "c-sharp": "// C#",
        "css": "/* CSS */",
        "cuda": "// Cuda",
        "fortran": "! Fortran",
        "go": "// Go",
        "html": "<!-- HTML -->",
        "java": "// Java",
        "js": "// JavaScript",
        "javascript": "// JavaScript",
        "kotlin": "// Kotlin",
        "lean": "-- Lean",
        "lua": "-- Lua",
        "objectivec": "// Objective-C",
        "objective-c": "// Objective-C",
        "objective-c++": "// Objective-C++",
        "pascal": "// Pascal",
        "php": "// PHP",
        "python": "# Python",
        "r": "# R",
        "rust": "// Rust",
        "ruby": "# Ruby",
        "scala": "// Scala",
        "shell": "# Shell",
        "sql": "-- SQL",
        "tex": f"% TeX",
        "typescript": "// TypeScript",
        "vue": "<!-- Vue -->",
        "assembly": "; Assembly",
        "dart": "// Dart",
        "perl": "# Perl",
        "prolog": f"% Prolog",
        "swift": "// swift",
        "lisp": "; Lisp",
        "vb": "' Visual Basic",
        "visual basic": "' Visual Basic",
        "matlab": f"% Matlab",
        "delphi": "{ Delphi }",
        "scheme": "; Scheme",
        "basic": "' Basic",
        "assembly": "; Assembly",
        "groovy": "// Groovy",
        "abap": "* Abap",
        "gdscript": "# GDScript",
        "haskell": "-- Haskell",
        "julia": "# Julia",
        "elixir": "# Elixir",
        "excel": "' Excel",
        "clojure": "; Clojure",
        "actionscript": "// ActionScript",
        "solidity": "// Solidity",
        "powershell": "# PowerShell",
        "erlang": f"% Erlang",
        "cobol": "// Cobol",
        "batchfile": ":: Batch file",
        "makefile": "# Makefile",
        "dockerfile": "# Dockerfile",
        "markdown": "<!-- Markdown -->",
        "cmake": "# CMake",
        "dockerfile": "# Dockerfile",
    }

    programming_languages_to_file_extensions = json.load(
        open("utils/programming-languages-to-file-extensions.json")
    )
    need2del = []
    for key in programming_languages_to_file_extensions.keys():
        if key.lower() not in LANGUAGE_TAG:
            need2del.append(key)

    for key in need2del:
        del programming_languages_to_file_extensions[key]

    ext_to_programming_languages = {}
    want_languages = []
    for key in programming_languages_to_file_extensions:
        for item in programming_languages_to_file_extensions[key]:
            ext_to_programming_languages[item] = key
            want_languages.append(item)

    ext = "." + obj.split(".")[-1]
    with open("utils/keep.txt", "r") as f:
        keep_files = f.readlines()
        keep_files = [l.strip() for l in keep_files]
    # print(ext)
    if ext not in want_languages:
        if obj in keep_files:
            return True
        return False
    else:
        return True
