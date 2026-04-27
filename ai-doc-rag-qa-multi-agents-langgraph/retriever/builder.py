from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from config.settings import settings
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

class RetrieverBuilder:
    def __init__(self):
        """Initialize the retriever builder with embeddings."""
        self.embeddings = OpenAIEmbeddings()
        
    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever using BM25 and vector-based retrieval."""
        try:
            docs = [d for d in docs if d.page_content and d.page_content.strip()]
            if not docs:
                raise ValueError("No valid documents to index after filtering empty chunks.")

            # Create Chroma vector store
            vector_store = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=settings.CHROMA_DB_PATH
            )
            logger.info("Vector store created successfully.")
            
            # Create BM25 retriever
            bm25 = BM25Retriever.from_documents(docs)
            logger.info("BM25 retriever created successfully.")
            
            # Create vector-based retriever
            vector_retriever = vector_store.as_retriever(search_kwargs={"k": settings.VECTOR_SEARCH_K})
            logger.info("Vector retriever created successfully.")
            
            # Combine retrievers into a hybrid retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25, vector_retriever],
                weights=settings.HYBRID_RETRIEVER_WEIGHTS
            )
            logger.info("Hybrid retriever created successfully.")
            return hybrid_retriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            raise