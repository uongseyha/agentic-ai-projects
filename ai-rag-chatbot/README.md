# AI-RAG-Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that lets users upload any PDF document and ask natural-language questions against it, powered by IBM watsonx.ai and LangChain.

## Demo Walkthrough

<video controls src="https://github.com/user-attachments/assets/a4f1bebd-1c02-4a2e-b8db-e24f00f253b6" title="AI RAG Chatbot Demo"></video>

---

## Problem Statement

Large Language Models (LLMs) are trained on fixed, general-purpose datasets. When users need answers from a **specific, private, or up-to-date document** (e.g., a contract, research paper, or manual), a bare LLM either hallucinates or simply cannot access that content.

Traditional keyword search is rigid and cannot understand the semantic meaning of questions. There is a gap between *having a document* and *being able to have a conversation with it*.

---

## Goal

Build a lightweight, local RAG chatbot that:

1. Accepts **any PDF** uploaded at runtime — no re-training needed.
2. Understands natural-language questions about that document.
3. Returns **grounded, document-cited answers** using an LLM, eliminating hallucination risk.
4. Provides a **simple web UI** accessible from a browser with no coding required from the end user.

---

## How It Works — Processing Pipeline

```
User uploads PDF
       │
       ▼
┌─────────────────┐
│  Document Loader │  PyPDFLoader reads and extracts text from all pages
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Splitter   │  Splits text into overlapping chunks (1000 chars / 50 overlap)
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Embedding Model      │  IBM watsonx slate-125m converts chunks → dense vectors
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  Vector Store (Chroma)│  Stores vectors in-memory for fast similarity search
└────────┬─────────────┘
         │
    User types query
         │
         ▼
┌──────────────────────┐
│  Retriever            │  Finds the top-k most semantically similar chunks
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  RetrievalQA Chain (LangChain)            │
│  Combines retrieved context + user query  │
│  into a prompt sent to the LLM            │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────┐
│  LLM                  │  IBM watsonx mistral-medium generates the final answer
└────────┬─────────────┘
         │
         ▼
    Answer displayed in Gradio UI
```

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        User Browser                           │
│                    Gradio Web UI (:7860)                       │
└────────────────────────┬────────────────────────┬────────────┘
                         │ PDF upload              │ Text query
                         ▼                         ▼
┌──────────────────────────────────────────────────────────────┐
│                        main.py  (entry point)                 │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    modules/                              │ │
│  │                                                          │ │
│  │  loader.py ──► splitter.py ──► embedding.py             │ │
│  │       │               │              │                   │ │
│  │       └───────────────┴──────► vectordb.py              │ │
│  │                                      │                   │ │
│  │                               retriever.py ◄─ llm.py    │ │
│  │                                      │                   │ │
│  │                                   app.py                 │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  IBM watsonx.ai (Cloud)                        │
│                                                               │
│   Embedding: ibm/slate-125m-english-rtrvr-v2                  │
│   LLM:       mistralai/mistral-medium-2505                    │
└──────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
ai-rag-chatbot/
├── main.py                 # Entry point — loads env, launches Gradio
├── requirements.txt        # Python dependencies
├── install.ps1             # PowerShell install script
├── .env                    # API keys (not committed)
├── .gitignore
└── modules/
    ├── __init__.py
    ├── llm.py              # WatsonxLLM configuration
    ├── loader.py           # PDF document loader
    ├── splitter.py         # Recursive text splitter
    ├── embedding.py        # Watsonx embedding model
    ├── vectordb.py         # Chroma vector store builder
    ├── retriever.py        # Retrieval chain + QA chain
    └── app.py              # Gradio interface definition
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | IBM watsonx.ai — `mistralai/mistral-medium-2505` | Answer generation |
| **Embeddings** | IBM watsonx.ai — `ibm/slate-125m-english-rtrvr-v2` | Text → vector conversion |
| **Orchestration** | LangChain (`langchain-ibm`, `langchain-community`, `langchain-classic`) | RAG pipeline / RetrievalQA chain |
| **Vector Store** | ChromaDB (in-memory) | Semantic similarity search |
| **Document Loader** | LangChain `PyPDFLoader` + `pypdf` | PDF text extraction |
| **Text Splitting** | LangChain `RecursiveCharacterTextSplitter` | Chunking documents |
| **UI** | Gradio | Browser-based web interface |
| **Config** | `python-dotenv` | Environment variable management |
| **Runtime** | Python 3.x + virtualenv | Local execution |

---

## Getting Started

### Prerequisites

- Python 3.9+
- IBM watsonx.ai account with an API key and Project ID

### Setup

```powershell
# 1. Clone the repo
git clone <repo-url>
cd ai-rag-chatbot

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
.\install.ps1

# 4. Configure environment variables
copy .env.example .env
# Edit .env and fill in your IBM_API_KEY and IBM_PROJECT_ID
```

### Run

```powershell
python main.py
```

Open your browser at `http://localhost:7860`, upload a PDF, type a question, and click **Submit**.

---

## Environment Variables

| Variable | Description |
|---|---|
| `IBM_API_KEY` | IBM Cloud API key for watsonx.ai |
| `IBM_PROJECT_ID` | watsonx.ai project ID |
