import os

from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores.faiss import FAISS, dependable_faiss_import
from models.embedding import GLMEmbeddings
from tqdm import tqdm
from utils.data import split_into_chunks

embed_model = GLMEmbeddings()


def vectorize(files: list[str], args):
    # split file into chunks
    chunks = []
    for file in tqdm(files, desc="文件切分"):
        chunks.extend(split_into_chunks(file, args.chunk_size, args.overlap_size))

    # initialize the vector store
    vector_store = FAISS(
        embedding_function=embed_model,
        index=dependable_faiss_import().IndexFlatL2(embed_model.embedding_size),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # translate to vectors
    batch_size = args.batch_size
    for i in tqdm(range(0, len(chunks), batch_size), desc="向量化"):
        try:
            vector_store.add_documents(chunks[i:i + batch_size])
        except Exception as e:
            print(f"文件向量化失败，{e}")

    # save embedded vectors
    output_path = args.output_path
    os.makedirs(output_path, exist_ok=True)
    vector_store.save_local(output_path)
    print(f"文件向量化完成，已保存至{output_path}")


def load_vector_store(vector_path: str):
    return FAISS.load_local(vector_path, embed_model, allow_dangerous_deserialization=True)
