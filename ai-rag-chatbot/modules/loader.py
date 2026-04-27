from langchain_community.document_loaders import PyPDFLoader


def document_loader(file):
    loader = PyPDFLoader(file.name)
    loaded_document = loader.load()
    return loaded_document
