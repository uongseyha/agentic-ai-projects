# AI Document RAG QA Multi-Agents on LangGraph

A document question-answering system that uses a multi-agent pipeline built on LangGraph to deliver accurate, verified answers from uploaded documents — rejecting off-topic queries and re-researching when answers fail verification.

---

## Demo Walkthrough

<video controls src="https://github.com/user-attachments/assets/68508387-6bd7-4fbc-a2f5-b6ac45b43ffc" title="AI Document RAG QA Multi-Agents on LangGraph"></video>

---

## Problem Statement

Traditional RAG-based Q&A pipelines suffer from several failure modes:

- **Hallucination** — the LLM fabricates facts not present in the source documents.
- **Irrelevant answers** — the system answers questions that have nothing to do with the uploaded documents, producing confident but wrong responses.
- **No quality gate** — once a draft answer is generated there is no mechanism to check whether it is actually supported by the retrieved context.

These problems erode trust in document Q&A tools, especially in high-stakes domains where factual accuracy matters (research, compliance, technical documentation).

---

## Objective

Build a self-correcting document Q&A system that:

1. **Refuses off-topic questions** before spending compute on them.
2. **Generates grounded answers** using only evidence retrieved from uploaded documents.
3. **Verifies every answer** for factual support, unsupported claims, and contradictions — and retries if the answer fails verification.
4. **Supports multiple document formats** (PDF, DOCX, TXT, Markdown) with a simple drag-and-drop web UI.

---

## Processing Flow

```
User uploads document(s) + enters question
          │
          ▼
  Document Processor (Docling)
  ┌─────────────────────────────┐
  │ 1. Parse file to Markdown   │
  │ 2. Split by Markdown headers│
  │ 3. Cache chunks (SHA-256)   │
  └────────────┬────────────────┘
               │
               ▼
   Hybrid Retriever Builder
  ┌─────────────────────────────┐
  │ BM25 (keyword)   weight 0.4 │
  │ ChromaDB (vector) weight 0.6│
  │ → EnsembleRetriever         │
  └────────────┬────────────────┘
               │
               ▼
      LangGraph Workflow
  ┌──────────────────────────────────────┐
  │                                      │
  │  [check_relevance]                   │
  │   RelevanceChecker asks GPT-4o-mini  │
  │   to classify: CAN_ANSWER /          │
  │   PARTIAL / NO_MATCH                 │
  │                                      │
  │   NO_MATCH ──────────────────► END   │
  │   (returns "not relevant" message)   │
  │                                      │
  │   CAN_ANSWER / PARTIAL               │
  │         │                            │
  │         ▼                            │
  │   [research]                         │
  │   ResearchAgent builds context from  │
  │   retrieved chunks → GPT-4o-mini     │
  │   generates draft answer             │
  │         │                            │
  │         ▼                            │
  │   [verify]                           │
  │   VerificationAgent checks draft     │
  │   against context:                   │
  │   • Supported: YES/NO                │
  │   • Unsupported Claims               │
  │   • Contradictions                   │
  │   • Relevant: YES/NO                 │
  │         │                            │
  │  Supported:NO ──────────────► research (retry)
  │  Relevant:NO  ──────────────► research (retry)
  │         │                            │
  │  All checks pass ───────────► END    │
  └──────────────────────────────────────┘
               │
               ▼
   Gradio UI displays:
   • Answer
   • Verification Report
```

---

## Architecture

```
ai-doc-rag-qa-multi-agents/
│
├── app.py                        # Gradio UI entry point (DocChat)
│
├── document_processor/
│   └── file_handler.py           # Docling parser, MarkdownHeaderTextSplitter, pickle cache
│
├── retriever/
│   └── builder.py                # BM25 + ChromaDB EnsembleRetriever
│
├── agents/
│   ├── workflow.py               # LangGraph StateGraph — orchestrates all agents
│   ├── relevance_checker.py      # Agent 1: classifies question vs. document relevance
│   ├── research_agent.py         # Agent 2: generates draft answer from retrieved context
│   └── verification_agent.py    # Agent 3: verifies draft answer for factual accuracy
│
├── config/
│   ├── settings.py               # Pydantic Settings (env-driven config)
│   └── constants.py              # File size limits, allowed types
│
├── utils/
│   └── logging.py                # Shared logger
│
├── examples/                     # Sample PDFs for demo
├── chroma_db/                    # Persisted ChromaDB vector store
├── document_cache/               # SHA-256 keyed pickle cache for processed chunks
└── requirements.txt
```

### LangGraph State Machine

```
                    ┌───────────────────┐
                    │   AgentState      │
                    │ • question        │
                    │ • documents       │
                    │ • draft_answer    │
                    │ • verif. report   │
                    │ • is_relevant     │
                    │ • retriever       │
                    └───────────────────┘

ENTRY ──► [check_relevance] ──(NO_MATCH)──► END
                │
           (CAN_ANSWER / PARTIAL)
                │
                ▼
          [research] ◄──────────────────────┐
                │                           │
                ▼                           │
           [verify] ──(Supported/Relevant: NO)──┘
                │
           (all pass)
                │
               END
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Workflow Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | OpenAI `gpt-4o-mini` (research, verification, relevance check) |
| Embeddings | OpenAI `text-embedding-ada-002` |
| Vector Store | [ChromaDB](https://www.trychroma.com/) (persisted locally) |
| Keyword Retrieval | BM25 (`langchain-community`) |
| Hybrid Retrieval | `EnsembleRetriever` (BM25 40% + Vector 60%) |
| Document Parsing | [Docling](https://github.com/DS4SD/docling) → Markdown |
| Text Splitting | `MarkdownHeaderTextSplitter` (LangChain) |
| Web UI | [Gradio](https://gradio.app/) |
| Configuration | Pydantic Settings (`.env` file) |
| Caching | SHA-256 pickle cache (7-day TTL) |
| Language | Python 3.12 |

---

## Agents

### 1. RelevanceChecker
Retrieves the top-20 chunks from the hybrid retriever and asks the LLM to classify whether the question can be answered from the document content. Returns one of:
- `CAN_ANSWER` — full information available, proceed.
- `PARTIAL` — topic mentioned but incomplete, proceed anyway.
- `NO_MATCH` — question is unrelated; workflow terminates with a rejection message.

### 2. ResearchAgent
Concatenates all retrieved document chunks into a single context string and prompts GPT-4o-mini to produce a concise, factual draft answer. Includes exponential-backoff retry on rate-limit errors (up to 5 attempts).

### 3. VerificationAgent
Takes the draft answer and the same document context, then asks GPT-4o-mini to produce a structured verification report:
- **Supported** — is the answer grounded in the context?
- **Unsupported Claims** — any claims not backed by the documents.
- **Contradictions** — any statements that conflict with the context.
- **Relevant** — does the answer address the question?

If `Supported: NO` or `Relevant: NO`, the workflow loops back to the ResearchAgent for a retry.

---

## Getting Started

### Prerequisites

- Python 3.12+
- OpenAI API key

### Installation

```bash
git clone <repo-url>
cd ai-doc-rag-qa-multi-agents
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
CHROMA_DB_PATH=./chroma_db
VECTOR_SEARCH_K=10
HYBRID_RETRIEVER_WEIGHTS=[0.4, 0.6]
CACHE_DIR=document_cache
CACHE_EXPIRE_DAYS=7
```

### Run

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser. Upload one or more documents (`.pdf`, `.docx`, `.txt`, `.md`), type a question, and click **Submit**.

---

## Example Queries

| Document | Example Question |
|---|---|
| Google 2024 Environmental Report | "Retrieve the data center PUE efficiency values in Singapore 2nd facility in 2019 and 2022. Also retrieve regional average CFE in Asia Pacific in 2023." |
| DeepSeek-R1 Technical Report | "Summarize DeepSeek-R1 model's performance evaluation on all coding tasks against OpenAI o1-mini model." |

Pre-loaded examples are available via the dropdown in the UI.