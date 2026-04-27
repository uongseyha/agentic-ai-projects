import os
from pathlib import Path
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

load_dotenv(Path(__file__).parent / ".env")

MODEL_ID = "mistralai/mistral-medium-2505"
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
IBM_API_KEY = os.environ.get("IBM_API_KEY")
IBM_PROJECT_ID = os.environ.get("IBM_PROJECT_ID")


def get_credentials() -> Credentials:
    return Credentials(url=WATSONX_URL, api_key=IBM_API_KEY)


def get_client() -> APIClient:
    return APIClient(get_credentials())


def get_llm_parameters() -> dict:
    return {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.MAX_NEW_TOKENS: 900,
    }
