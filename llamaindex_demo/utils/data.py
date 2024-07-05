import os
from pathlib import Path

from llama_index.core.node_parser import CodeSplitter
from llama_index.core.schema import BaseNode
from llama_index.readers.file import FlatReader

Languages = {
    'c': "c",
    'cpp': "cpp",
    'go': "go",
    'java': "java",
    'js': "javascript",
    'md': "markdown",
    'py': "python",
    'ts': "typescript",
}


def traverse(repo_path: str) -> list[str]:
    """
    Traverse the directory, fetch all files
    - skip hidden directories
    - only keep the supported files
    :param repo_path: path to this repo
    """

    def helper(root):
        for entry in os.scandir(root):
            if entry.name.startswith('.'):
                continue
            if entry.is_file():
                ext = entry.name.split('.')[-1].lower()
                if ext not in Languages.keys():
                    continue
                file_paths.append(entry.path)
            elif entry.is_dir():
                helper(entry.path)

    file_paths = []
    helper(repo_path)
    return sorted(file_paths)


def split_into_chunks(file_path, lines_per_chunk, lines_overlap, max_chars) -> list[BaseNode]:
    """
    Split file into chunks
    :param file_path: path to the file
    :param lines_per_chunk: lines for each chunk
    :param lines_overlap: overlap lines between 2 chunks
    :param max_chars: max characters for each chunk
    """
    ext = file_path.split('.')[-1].lower()
    lang = Languages.get(ext, None)
    if not lang:
        return []
    try:
        documents = FlatReader().load_data(Path(file_path))
        splitter = CodeSplitter(
            language=lang,
            chunk_lines=lines_per_chunk,
            chunk_lines_overlap=lines_overlap,
            max_chars=max_chars,
        )
        return splitter.get_nodes_from_documents(documents)
    except Exception as e:
        print(f'`{file_path}`切分失败: {e}')
        return []
