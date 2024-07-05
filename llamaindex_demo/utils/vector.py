import os

import faiss
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.legacy.vector_stores import FaissVectorStore
from models.embedding import GLMEmbeddings
from tqdm import tqdm
from utils.data import split_into_chunks

embed_model = GLMEmbeddings()


def save_vectors(files: list[str], args):
    # split file into chunks
    nodes = []
    for file in tqdm(files, desc="文件切分"):
        nodes.extend(split_into_chunks(file, args.lines_per_chunk, args.lines_overlap, args.max_chars))

    # initialize vector store
    vector_store = FaissVectorStore(faiss_index=faiss.IndexFlatL2(embed_model.embedding_size))
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # translate to vectors
    index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, embed_model=embed_model)

    # save embedded vectors
    output_path = args.output_path
    os.makedirs(output_path, exist_ok=True)
    index.storage_context.persist(persist_dir=output_path)
    print(f"文件向量化完成，已保存至{output_path}")


def load_vectors(vector_path: str):
    vector_store = FaissVectorStore.from_persist_dir(vector_path)
    storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=vector_path)
    return load_index_from_storage(storage_context=storage_context)
