import os
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from langchain_ibm import WatsonxLLM


def get_llm():
    model_id = 'mistralai/mistral-medium-2505'
    parameters = {
        GenParams.MAX_NEW_TOKENS: 256,
        GenParams.TEMPERATURE: 0.5,
    }
    project_id = os.environ["IBM_PROJECT_ID"]
    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        apikey=os.environ["IBM_API_KEY"],
        project_id=project_id,
        params=parameters,
    )
    return watsonx_llm
