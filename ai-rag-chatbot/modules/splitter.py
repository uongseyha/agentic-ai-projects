from langchain_text_splitters import RecursiveCharacterTextSplitter


def text_splitter(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = splitter.split_documents(data)
    return chunks
