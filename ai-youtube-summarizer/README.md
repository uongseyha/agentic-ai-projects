# AI RAG YouTube Summarizer

A Retrieval-Augmented Generation (RAG) application that extracts YouTube video transcripts and uses IBM WatsonX foundation models to generate summaries and answer natural language questions about the video content.

---

## Demo Walkthrough

<video controls src="https://github.com/user-attachments/assets/bb68e300-f441-4bc5-a449-3aeaf3294ae6" title="AI RAG YouTube Summarizer"></video>

---
## Problem Statement

Watching long YouTube videos to extract key information is time-consuming. Viewers often need to:
- Quickly understand what a video covers before committing to watching it in full.
- Find specific answers buried inside hour-long lectures, tutorials, or talks.

Manually scrubbing through transcripts or timestamps is inefficient. There is no native YouTube feature that summarizes content or answers user-specific questions about a video.

---

## Goal

Build a web application that:
1. Accepts any YouTube video URL with an English transcript.
2. Generates a concise, AI-produced **summary** of the video in one click.
3. Allows users to ask **natural language questions** about the video and receive accurate, context-grounded answers — without hallucination from unrelated knowledge.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Gradio Web UI                            │
│   [ YouTube URL ]  [ Summarize ]  [ Question ]  [ Ask ]         │
└──────────────┬──────────────────────────────┬───────────────────┘
               │                              │
               ▼                              ▼
   ┌───────────────────┐          ┌───────────────────────┐
   │  Summarize Flow   │          │     Q&A Flow (RAG)    │
   └────────┬──────────┘          └──────────┬────────────┘
            │                               │
            ▼                               ▼
   ┌─────────────────────────────────────────────────┐
   │              transcript.py                      │
   │  YouTube URL → video ID → YouTubeTranscriptApi  │
   │  → fetch English transcript → format text       │
   └─────────────────────┬───────────────────────────┘
                         │
            ┌────────────┴─────────────┐
            │ Summarize                │ Q&A
            ▼                          ▼
   ┌──────────────────┐     ┌────────────────────────────┐
   │  Full transcript │     │  RecursiveCharacterText-   │
   │  sent to prompt  │     │  Splitter → chunks (200    │
   └────────┬─────────┘     │  tokens, 20 overlap)       │
            │               └──────────┬─────────────────┘
            │                          │
            │               ┌──────────▼─────────────────┐
            │               │  WatsonxEmbeddings          │
            │               │  ibm/slate-30m-english-     │
            │               │  rtrvr-v2                   │
            │               └──────────┬─────────────────┘
            │                          │
            │               ┌──────────▼─────────────────┐
            │               │  FAISS Vector Index         │
            │               │  similarity_search(k=7)     │
            │               └──────────┬─────────────────┘
            │                          │
            ▼                          ▼
   ┌─────────────────────────────────────────────────┐
   │              chains.py                          │
   │  PromptTemplate → LLMChain                      │
   │  WatsonxLLM (mistralai/mistral-medium-2505)     │
   │  Greedy decoding, max 900 new tokens            │
   └─────────────────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Summary / Answer  │
              │   returned to UI    │
              └─────────────────────┘
```

---

## Processing Detail

### Summarization Flow

1. **URL validation** — regex extracts the 11-character YouTube video ID.
2. **Transcript fetch** — `YouTubeTranscriptApi` lists available transcripts; manually-created English transcripts are preferred over auto-generated ones.
3. **Text formatting** — each transcript entry is serialised as `Text: <spoken words> Start: <timestamp>`.
4. **Prompt construction** — the full formatted transcript is injected into a system/user prompt instructing the LLM to produce a single concise paragraph, ignoring timestamps.
5. **LLM generation** — `WatsonxLLM` (Mistral Medium) generates the summary via greedy decoding.

### Q&A Flow (RAG)

1. **Transcript fetch** — same as above; cached between calls if already fetched for the same session.
2. **Chunking** — `RecursiveCharacterTextSplitter` splits the transcript into 200-character chunks with 20-character overlap, preserving sentence boundaries.
3. **Embedding** — each chunk is embedded with `WatsonxEmbeddings` using the `ibm/slate-30m-english-rtrvr-v2` model.
4. **FAISS index** — embeddings are stored in an in-memory FAISS index for fast nearest-neighbour lookup.
5. **Retrieval** — the user's question is embedded and the top-7 most similar chunks are retrieved.
6. **Answer generation** — the retrieved context and the question are injected into a Q&A prompt; `WatsonxLLM` generates a grounded answer.

---

## Project Structure

```
ai-youtube-summarizer/
├── app.py            # Gradio UI and orchestration
├── config.py         # Credentials, model IDs, LLM parameters
├── transcript.py     # YouTube transcript fetching and text processing
├── llm.py            # WatsonxLLM and WatsonxEmbeddings instantiation
├── vector_store.py   # FAISS index creation and similarity search
├── chains.py         # Prompt templates, LLM chains, generation helpers
├── requirements.txt  # Python dependencies
└── .env              # API keys and project ID (not committed)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **UI** | [Gradio](https://www.gradio.app/) |
| **Transcript extraction** | [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) |
| **Text splitting** | LangChain `RecursiveCharacterTextSplitter` (`langchain-text-splitters`) |
| **Embeddings** | IBM WatsonX `ibm/slate-30m-english-rtrvr-v2` (`langchain-ibm`) |
| **Vector store** | [FAISS](https://github.com/facebookresearch/faiss) (`faiss-cpu`) |
| **LLM** | IBM WatsonX `mistralai/mistral-medium-2505` (`langchain-ibm`) |
| **LLM orchestration** | LangChain `LLMChain` + `PromptTemplate` (`langchain-classic`) |
| **IBM platform SDK** | `ibm-watsonx-ai` |
| **Config / secrets** | `python-dotenv` |
| **Language** | Python 3.12 |

---

## Setup

### Prerequisites

- Python 3.12+
- An [IBM Cloud](https://cloud.ibm.com/) account with a WatsonX project

### Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```dotenv
IBM_API_KEY=<your-ibm-cloud-api-key>
IBM_PROJECT_ID=<your-watsonx-project-id>
```

### Run

```bash
python app.py
```

The app will be available at `http://localhost:7860`.
