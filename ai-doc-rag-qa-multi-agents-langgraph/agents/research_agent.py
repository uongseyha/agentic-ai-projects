from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Dict, List
from langchain_core.documents import Document
import time
from dotenv import load_dotenv

load_dotenv()


class ResearchAgent:
    def __init__(self):
        print("Initializing ResearchAgent with OpenAI...")
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, max_tokens=300)
        print("Model initialized successfully.")

    def sanitize_response(self, response_text: str) -> str:
        return response_text.strip()

    def generate_prompt(self, question: str, context: str) -> str:
        return f"""
        You are an AI assistant designed to provide precise and factual answers based on the given context.

        **Instructions:**
        - Answer the following question using only the provided context.
        - Be clear, concise, and factual.
        - Return as much information as you can get from the context.

        **Question:** {question}
        **Context:**
        {context}

        **Provide your answer below:**
        """

    def generate(self, question: str, documents: List[Document]) -> Dict:
        print(f"ResearchAgent.generate called with question='{question}' and {len(documents)} documents.")

        context = "\n\n".join([doc.page_content for doc in documents])
        print(f"Combined context length: {len(context)} characters.")

        prompt = self.generate_prompt(question, context)

        max_retries = 5
        for attempt in range(max_retries):
            try:
                print("Sending prompt to the model...")
                response = self.model.invoke([HumanMessage(content=prompt)])
                print("LLM response received.")
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"Rate limit hit, retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                else:
                    print(f"Error during model inference: {e}")
                    raise RuntimeError("Failed to generate answer due to a model error.") from e

        llm_response = response.content.strip()
        print(f"Raw LLM response:\n{llm_response}")

        draft_answer = self.sanitize_response(llm_response) if llm_response else "I cannot answer this question based on the provided documents."
        print(f"Generated answer: {draft_answer}")

        return {
            "draft_answer": draft_answer,
            "context_used": context
        }
