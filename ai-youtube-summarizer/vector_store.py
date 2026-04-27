from langchain_community.vectorstores import FAISS
from langchain_ibm import WatsonxEmbeddings


def build_faiss_index(chunks: list[str], embedding_model: WatsonxEmbeddings) -> FAISS:
    return FAISS.from_texts(chunks, embedding_model)


def similarity_search(faiss_index: FAISS, query: str, k: int = 3) -> list:
    return faiss_index.similarity_search(query, k=k)
