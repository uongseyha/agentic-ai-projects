from ibm_watsonx_ai import Credentials
from langchain_ibm import WatsonxLLM, WatsonxEmbeddings
from config import IBM_API_KEY, IBM_PROJECT_ID, MODEL_ID, WATSONX_URL, get_llm_parameters

EMBEDDING_MODEL_ID = "ibm/slate-30m-english-rtrvr-v2"


def get_llm(credentials: Credentials | None = None) -> WatsonxLLM:
    url = credentials.get("url") if credentials else WATSONX_URL
    return WatsonxLLM(
        model_id=MODEL_ID,
        url=url,
        apikey=IBM_API_KEY,
        project_id=IBM_PROJECT_ID,
        params=get_llm_parameters(),
    )


def get_embedding_model(credentials: Credentials | None = None) -> WatsonxEmbeddings:
    url = credentials["url"] if credentials else WATSONX_URL
    return WatsonxEmbeddings(
        model_id=EMBEDDING_MODEL_ID,
        url=url,
        apikey=IBM_API_KEY,
        project_id=IBM_PROJECT_ID,
    )
