# GenAI Projects

A collection of Generative AI projects built with LLMs, RAG pipelines, and modern AI frameworks. Each project demonstrates a different aspect of applied generative AI — from fine-tuning open-source models to building production-style chatbots and document Q&A systems.

## Table of Contents

- [Projects Overview](#projects-overview)
- [Projects](#projects)
  - [LLM Fine-Tuning (Llama 2)](#1-llm-fine-tuning-llama-2)
  - [Interview Question Generator](#2-interview-question-generator)
  - [Medical Chatbot](#3-medical-chatbot)
  - [Web Bot](#4-web-bot)
  - [Website Chatbot Notebook](#5-website-chatbot-notebook)
  - [Zomato Chatbot](#6-zomato-chatbot)
- [Tech Stack Summary](#tech-stack-summary)
- [Author](#author)

---

## Projects Overview

| Project | Type | Framework | LLM | Status |
|---|---|---|---|---|
| [LLM Fine-Tuning](#1-llm-fine-tuning-llama-2) | Notebook | Hugging Face / TRL | Llama-2-7B | ✅ Complete |
| [Interview Question Generator](#2-interview-question-generator) | Web App | FastAPI | HuggingFace Hub | ✅ Complete |
| [Medical Chatbot](#3-medical-chatbot) | Web App | Flask | NVIDIA Llama-3.1-70B | ✅ Complete |
| [Web Bot](#4-web-bot) | Web App | LangChain | Any | [In Development] |
| [Website Chatbot Notebook](#5-website-chatbot-notebook) | Notebook | LangChain | HuggingFace Hub | ✅ Complete |
| [Zomato Chatbot](#6-zomato-chatbot) | Web App | Chainlit | OpenAI-compatible | ✅ Complete |

---

## Projects

### 1. LLM Fine-Tuning (Llama 2)

**Directory:** `Finetuning/`

Fine-tunes the **Llama-2-7B** model on custom datasets using parameter-efficient techniques. Designed for Google Colab with GPU support.

**Key Features:**
- 4-bit quantization with BitsAndBytes to reduce GPU memory usage
- LoRA (Low-Rank Adaptation) via `peft` — `r=16`, `lora_alpha=32`
- Supervised Fine-Tuning (SFT) using TRL's `SFTTrainer`
- Trains on the `mlabonne/guanaco-llama2-1k` dataset

**Technologies:** `transformers`, `peft`, `trl`, `bitsandbytes`, `accelerate`, `datasets`, Hugging Face Hub

**Notebooks:**
- `Llama_2.ipynb` — Full fine-tuning pipeline
- `experiment.ipynb` — Experimental notebook

---

### 2. Interview Question Generator

**Directory:** `Interview_question_generator/`

A **FastAPI** web application that extracts text from uploaded PDF documents and automatically generates interview questions using LangChain and optional HuggingFace LLM enhancement.

**Key Features:**
- Drag-and-drop PDF upload via a Jinja2-rendered web UI
- Text extraction with PyPDF2
- Key topic and concept identification
- AI-powered question generation (simple or HuggingFace-backed)
- Download results as CSV

**Technologies:** `FastAPI`, `LangChain`, `FAISS`, `PyPDF2`, `tiktoken`, `HuggingFace Hub`, `Jinja2`, `aiofiles`

**API Endpoints:**
- `GET /` — Home page
- `POST /upload` — Upload a PDF
- `POST /generate` — Generate questions from uploaded PDF
- `GET /docs` — Swagger UI

**Setup:**
```bash
cd Interview_question_generator
pip install -r Requirements.txt
uvicorn src.app:app --reload
```

---

### 3. Medical Chatbot

**Directory:** `Medical_chatbot/`

A **RAG (Retrieval-Augmented Generation)** chatbot that answers medical questions by semantically searching local PDF medical documents and generating responses with NVIDIA's Llama-3.1-70B model.

**Key Features:**
- PDF ingestion, chunking (500 chars / 20 overlap), and embedding generation
- Semantic vector storage and retrieval using **Pinecone**
- Embeddings via `sentence-transformers/all-MiniLM-L6-v2`
- LLM responses from `meta/llama-3.1-70b-instruct` via NVIDIA AI Endpoints
- Flask-based chat web interface

**Technologies:** `Flask`, `LangChain`, `Pinecone`, `NVIDIA AI Endpoints`, `sentence-transformers`, `pypdf`, `python-dotenv`

**Environment Variables:**
```
PINECONE_API_KEY=<your_key>
NVIDIA_API_KEY=<your_key>
PINECONE_INDEX_NAME=medicalbot
```

**Setup:**
```bash
cd Medical_chatbot
pip install -r requirements.txt
python store_index.py   # Index PDFs into Pinecone
python app.py           # Start Flask server
```

---

### 4. Web Bot

**Directory:** `Web_bot/`

A website Q&A chatbot built on a **RAG architecture** that crawls website content via sitemap, indexes it into a vector store, and answers user questions using a configurable LLM.

**Key Features:**
- Sitemap crawling and content extraction
- Chunked document indexing with FAISS or Pinecone
- Semantic search and LLM-powered responses
- Supports OpenAI, HuggingFace, or local models

**Technologies:** `LangChain`, `sentence-transformers`, `Pinecone`, `FAISS`, `unstructured`, `transformers`

> **Status:** Architecture and notebook structure available; full implementation in progress.

---

### 5. Website Chatbot Notebook

**File:** `website_chatbot.ipynb`

A **Google Colab** notebook demonstrating a RAG chatbot that loads content directly from website URLs, indexes it with FAISS, and answers questions using HuggingFace models.

**Key Features:**
- URL-based content loading with `UnstructuredURLLoader`
- Text splitting with `CharacterTextSplitter`
- FAISS vector store for fast retrieval
- HuggingFace embeddings and LLM responses

**Technologies:** `LangChain`, `FAISS`, `HuggingFaceEmbeddings`, `HuggingFaceHub`, `unstructured`, `tiktoken`

**Quick Start (Google Colab):**
```python
# All install commands are included in the notebook cells
# Simply open in Colab and run all cells
```

---

### 6. Zomato Chatbot

**Directory:** `zomato_chatbot/`

A food discovery chatbot powered by **Chainlit** that connects to any OpenAI-compatible LLM endpoint and provides a graceful rule-based fallback when the LLM is unavailable.

**Key Features:**
- Works with any OpenAI-compatible API endpoint (OpenAI, Azure, local models, etc.)
- Rule-based fallback system for resilient responses
- Modern chat UI via Chainlit
- Fully configurable via environment variables

**Technologies:** `Chainlit`, `OpenAI Python SDK`, `python-dotenv`

**Environment Variables:**
```
LLM_API_KEY=<your_key>          # or OPENAI_API_KEY
LLM_MODEL=gpt-4o-mini           # default
LLM_BASE_URL=https://api.openai.com/v1   # default
LLM_TIMEOUT_SECONDS=25          # default
```

**Setup:**
```bash
cd zomato_chatbot
pip install -r requirements.txt
chainlit run app.py
# Opens at http://localhost:8000
```

---

## Tech Stack Summary

| Category | Technologies |
|---|---|
| **LLM Frameworks** | LangChain, Hugging Face Transformers, NVIDIA AI Endpoints, OpenAI SDK |
| **Vector Databases** | Pinecone, FAISS, ChromaDB |
| **Web Frameworks** | FastAPI, Flask, Chainlit |
| **Embeddings** | sentence-transformers, HuggingFace Embeddings, OpenAI Embeddings |
| **PDF Processing** | PyPDF2, pypdf, unstructured |
| **Fine-Tuning** | peft (LoRA), trl (SFT), bitsandbytes (quantization) |
| **Others** | Jinja2, aiofiles, tiktoken, python-dotenv |

---

## Author

**Tamaghna Sarkar** — [tamaghna51@gmail.com](mailto:tamaghna51@gmail.com)

