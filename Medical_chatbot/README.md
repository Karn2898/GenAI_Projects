# Medical Chatbot using Flask,LangChain, Pinecone , NVIDIA NIM

This project is a Retrieval-Augmented Generation (RAG) medical chatbot.
It answers user questions by retrieving relevant chunks from local medical PDF files and passing that context to an LLM.

## What I Built

The chatbot is built as a classic RAG pipeline with these layers:

1. Data ingestion and chunking
- PDF files are loaded from the `data/` folder.
- Documents are split into smaller chunks for retrieval.
- Implementation: `src/helper.py`

2. Embedding generation
- Each chunk is converted into vectors using Hugging Face embeddings.
- Model used: `sentence-transformers/all-MiniLM-L6-v2`
- Implementation: `src/helper.py`

3. Vector storage
- Vectors are stored in a Pinecone index.
- Index creation and population happen in `store_index.py`.
- Default index name: `medicalbot` (can be overridden with env var).

4. Retrieval + generation
- Flask endpoint receives user question.
- Top matching chunks are retrieved from Pinecone.
- Retrieved context is sent to NVIDIA LLM through LangChain.
- LLM used: `meta/llama-3.1-70b-instruct`
- Main app implementation: `app.py`

5. Prompting and UI
- System prompt is stored in `src/prompt.py`.
- Frontend template is in `templates/chat.html` with styles in `static/style.css`.

## Project Structure

```
Medical-chatbot/
|-- app.py
|-- store_index.py
|-- requirements.txt
|-- data/
|-- src/
|   |-- helper.py
|   |-- prompt.py
|-- templates/
|   |-- chat.html
|-- static/
|   |-- style.css
```

## Prerequisites

- Python 3.10+ (tested with Python 3.12)
- A Pinecone account and API key
- NVIDIA API key for `langchain-nvidia-ai-endpoints`

## Setup

1. Clone the repository and open it in your terminal.

2. Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\.venv\Scripts\Activate.ps1
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in project root:

```env
PINECONE_API_KEY=your_pinecone_key
NVIDIA_API_KEY=your_nvidia_key
PINECONE_INDEX_NAME=medicalbot
```

## How to Run

Step 1: Put your medical PDFs in the `data/` directory.

Step 2: Build/populate the Pinecone index.

```bash
python store_index.py
```

Step 3: Start the Flask app.

```bash
python app.py
```

Step 4: Open your browser:

http://localhost:8080

## Runtime Flow

When the app runs:

1. `app.py` loads API keys from `.env`.
2. Connects to existing Pinecone index.
3. Creates retriever with top-k similarity search (`k=3`).
4. Builds RAG chain using:
- retrieval chain
- document combine chain
- system prompt from `src/prompt.py`
5. User messages are sent to `/get`, answered, and returned to UI.

## Common Issues

1. Missing API keys
- Error: missing `PINECONE_API_KEY` or `NVIDIA_API_KEY`
- Fix: ensure `.env` exists at project root and contains both keys.

2. Pinecone index unavailable
- Error at startup says index is unavailable.
- Fix: run `python store_index.py` first, then restart app.

3. PowerShell activation blocked
- If script execution is disabled, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

4. No answers / poor answers
- Ensure PDFs are present in `data/` before running `store_index.py`.
- Rebuild index if documents changed.

## Tech Stack

- Flask
- LangChain
- Pinecone Vector DB
- NVIDIA AI Endpoints
- Hugging Face sentence-transformers

## Future Improvements

- Add chat history memory
- Add source citations in responses
- Add Docker support
- Add automated tests
