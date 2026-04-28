# Project List

<p align="center">
  <img src="https://img.shields.io/badge/AI-Agentic%20Projects-5-orange" alt="Projects">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

---

A collection of AI-powered agentic applications demonstrating various LLM agent architectures, RAG implementations, and multi-modal AI solutions.

---

## 📁 Projects Overview

| # | Project | Description | Key Tech |
|---|---------|-------------|----------|
| 1 | [ai-nutrition-coach-multi-agents-multimodal-crewai](#1-ai-nutrition-coach-multi-agents-multimodal-crewai) | Multi-agent nutrition coach that analyzes food images, provides nutritional insights, and generates recipe suggestions | CrewAI, GPT-4o Vision, Gradio |
| 2 | [ai-doc-rag-qa-multi-agents-langgraph](#2-ai-doc-rag-qa-multi-agents-langgraph) | Self-correcting document Q&A system with multi-agent pipeline, verification, and relevance checking | LangGraph, LangChain, ChromaDB |
| 3 | [ai-rag-chatbot](#3-ai-rag-chatbot) | PDF chatbot using RAG for natural language Q&A against uploaded documents | IBM watsonx, LangChain, ChromaDB |
| 4 | [ai-youtube-summarizer](#4-ai-youtube-summarizer) | YouTube video summarizer and Q&A using transcript-based RAG | IBM watsonx, Gradio, FAISS |
| 5 | [ai-youtube-summarizer](#5-ai-youtube-summarizer) | (See #4) | |

---

## 📋 Project Details

### 1. AI-Nutrition-Coach-Multi-Agents-Multimodal-CrewAI

| Category | Details |
|----------|---------|
| **Description** | Multi-agent AI nutrition coach that uses computer vision to analyze food images, detect ingredients, filter by dietary restrictions, analyze nutrition, and generate recipe suggestions |
| **Architecture** | CrewAI multi-agent framework with 4 specialized agents |
| **Agents** | Vision AI Specialist, Nutritionist AI Specialist, Nutrition Analysis Specialist, Recipe Generation Specialist |
| **Tech Stack** | `CrewAI`, `Gradio`, `OpenAI GPT-4o`, `Pydantic`, `PyYAML` |
| **Input** | Food images (JPG, PNG) |
| **Output** | Ingredient detection, nutritional analysis, recipe suggestions |

```python
# Key Components
- ExtractIngredientsTool    # GPT-4o vision for ingredient detection
- DietaryFilterTool         # LLM-based dietary restriction filtering
- NutrientAnalysisTool     # Nutritional breakdown & calorie estimation
- RecipeSuggestionAgent    # Recipe generation from filtered ingredients
```

---

### 2. AI-Doc-RAG-QA-Multi-Agents-LangGraph

| Category | Details |
|----------|---------|
| **Description** | Self-correcting document Q&A system that uses multi-agent pipeline to deliver accurate, verified answers from uploaded documents — rejects off-topic queries and re-researches on verification failure |
| **Architecture** | LangGraph state machine with 3 specialized agents |
| **Agents** | Research Agent, Relevance Checker Agent, Verification Agent |
| **Tech Stack** | `LangGraph`, `LangChain`, `ChromaDB`, `Docling`, `Gradio` |
| **Input** | PDF, DOCX, TXT, Markdown documents |
| **Output** | Grounded, verified answers with source citations |

```python
# Key Components
- DocumentProcessor    # Parse files to Markdown, split by headers, cache with SHA-256
- HybridRetriever      # BM25 + embedding-based hybrid search
- RelevanceChecker    # Determines if question is relevant to document
- VerificationAgent   # Verifies answer against retrieved context
```

---

### 3. AI-RAG-Chatbot

| Category | Details |
|----------|---------|
| **Description** | Lightweight RAG chatbot that lets users upload any PDF and ask natural-language questions against it, powered by IBM watsonx.ai and LangChain |
| **Architecture** | Single-pipeline RAG with document processing and semantic search |
| **Tech Stack** | `IBM watsonx.ai`, `LangChain`, `ChromaDB`, `Gradio`, `PyPDFLoader` |
| **Input** | PDF documents |
| **Output** | Grounded answers with document citations |

```python
# Key Components
- PyPDFLoader          # Extract text from PDF pages
- TextSplitter         # Split into overlapping chunks (1000 chars / 50 overlap)
- watsonx Embeddings  # IBM slate-125m model for vectorization
- ChromaDB             # Vector store for similarity search
- watsonx LLM          # Generate answers from retrieved context
```

---

### 4. AI-YouTube-Summarizer

| Category | Details |
|----------|---------|
| **Description** | RAG application that extracts YouTube video transcripts and uses IBM WatsonX foundation models to generate summaries and answer natural language questions about video content |
| **Architecture** | Dual-flow: Summarize flow + Q&A flow (RAG) |
| **Tech Stack** | `IBM watsonx.ai`, `Gradio`, `YouTubeTranscriptApi`, `FAISS` |
| **Input** | YouTube video URLs (with English transcripts) |
| **Output** | AI-generated video summaries, contextual Q&A answers |

```python
# Key Components
- transcript.py        # Extract English transcripts from YouTube videos
- chains.py            # LLM chains for summarization and Q&A
- vector_store.py     # FAISS index for semantic search over transcripts
- watsonx LLMs        # Granite & Slate models for generation
```

---

## 🛠️ Tech Stack Summary

| Technology | Projects | Usage |
|------------|----------|-------|
| **CrewAI** | #1 | Multi-agent orchestration |
| **LangGraph** | #2 | State machine & agent workflows |
| **LangChain** | #2, #3 | RAG pipeline & chain abstractions |
| **OpenAI GPT-4o** | #1 | Vision & text processing |
| **IBM watsonx.ai** | #3, #4 | LLM & embeddings |
| **ChromaDB** | #2, #3 | Vector database |
| **FAISS** | #4 | Vector similarity search |
| **Gradio** | #1, #2, #3, #4 | Web UI |
| **Pydantic** | #1 | Data validation |
| **PyYAML** | #1 | Configuration |

---

## 🚀 Quick Start

```bash
# Navigate to any project
cd ai-nutrition-coach-multi-agents-multimodal-crewai

# Install dependencies
pip install -r requirements.txt

# Configure API keys
# Create .env file with required keys (OPENAI_API_KEY, etc.)

# Run the application
python app.py
```

---

## 📂 Project Structure

```
agentic-ai-projects/
├── README.md
├── requirements.txt
├── ai-nutrition-coach-multi-agents-multimodal-crewai/
│   ├── app.py              # Gradio UI
│   ├── src/
│   │   ├── crew.py         # CrewAI crews
│   │   ├── tools.py        # Custom tools
│   │   ├── models.py       # Pydantic models
│   │   └── config/        # Agent & task configs
│   └── examples/
├── ai-doc-rag-qa-multi-agents-langgraph/
│   ├── app.py
│   ├── agents/             # Agent implementations
│   ├── retriever/          # Retrieval logic
│   └── chroma_db/          # Vector store
├── ai-rag-chatbot/
│   ├── main.py
│   └── modules/           # Loader, splitter, retriever, etc.
└── ai-youtube-summarizer/
    ├── app.py
    ├── chains.py
    └── transcript.py
```

---

## 🔑 Key Features

| Project | Features |
|---------|----------|
| #1 | Image-based ingredient detection, dietary filtering, nutritional analysis, recipe generation |
| #2 | Multi-agent verification, relevance checking, self-correcting pipeline, multi-format support |
| #3 | PDF upload at runtime, natural language Q&A, grounded answers with citations |
| #4 | YouTube transcript extraction, AI summarization, contextual Q&A without hallucination |

---

## 📄 License

MIT License - See individual project READMEs for details
