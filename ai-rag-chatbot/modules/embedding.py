import os
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings


def watsonx_embedding():
    embed_params = {
        EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
        EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
    }
    embedding = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr-v2",
        url="https://us-south.ml.cloud.ibm.com",
        apikey=os.environ["IBM_API_KEY"],
        project_id=os.environ["IBM_PROJECT_ID"],
        params=embed_params,
    )
    return embedding
