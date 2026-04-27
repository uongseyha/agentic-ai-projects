from langchain_classic.chains import RetrievalQA
from .llm import get_llm
from .loader import document_loader
from .splitter import text_splitter
from .vectordb import vector_database


def retriever(file):
    splits = document_loader(file)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    return vectordb.as_retriever()


def retriever_qa(file, query):
    llm = get_llm()
    retriever_obj = retriever(file)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=False,
    )
    response = qa.invoke(query)
    return response['result']
