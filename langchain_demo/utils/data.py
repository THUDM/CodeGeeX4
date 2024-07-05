import os

from langchain.text_splitter import (
    Language,
    RecursiveCharacterTextSplitter as TextSplitter,
)
from langchain_community.document_loaders import TextLoader

Languages = {
    'c': Language.CPP,
    'cpp': Language.CPP,
    'go': Language.GO,
    'java': Language.JAVA,
    'js': Language.JS,
    'md': Language.MARKDOWN,
    'py': Language.PYTHON,
    'ts': Language.TS,
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


def split_into_chunks(file_path, chunk_size, overlap_size) -> list[str]:
    """
    Split file into chunks
    :param file_path: path to the file
    :param chunk_size: size for each chunk
    :param overlap_size: overlap size betweeen 2 chunks
    """
    ext = file_path.split('.')[-1].lower()
    lang = Languages.get(ext, None)
    if not lang:
        return []
    try:
        loader = TextLoader(file_path, encoding='utf-8', autodetect_encoding=True)
        splitter = TextSplitter.from_language(lang, chunk_size=chunk_size, chunk_overlap=overlap_size)
        return loader.load_and_split(splitter)
    except Exception as e:
        print(f'`{file_path}`切分失败: {e}')
        return []
