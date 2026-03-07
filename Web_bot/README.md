# Web_bot
A website chatbot powered by Retrieval Augmented Generation (RAG) architecture.

## Overview
This project implements an intelligent chatbot that can answer questions about any website's content by indexing the site's pages and using semantic search with LLM-powered responses.

## Project Architecture

```mermaid
flowchart TB
    subgraph "Phase 1: Data Collection & Indexing"
        A[Website] -->|Crawl| B[Sitemap Collection]
        B --> C[Extract Page Content]
        C --> D[Documents/Chunks]
        D --> E[Embedding Model]
        E --> F[Vector Embeddings]
        F --> G[Semantic Index]
        G --> H[(Knowledge Base)]
    end
    
    subgraph "Phase 2: Query Processing & Response"
        I[User Question] --> J[Embedding Model]
        J --> K[Query Embedding]
        K --> L[Semantic Search]
        H -.->|Retrieve| L
        L --> M[Ranked Results]
        M --> N[LLM]
        I -.->|Context| N
        N --> O[Generated Response]
        O --> P[User]
    end
    
    style H fill:#4CAF50
    style N fill:#2196F3
    style E fill:#FF9800
    style J fill:#FF9800
```

## System Workflow

### Phase 1: Indexing (Data Ingestion)
1. **Sitemap Collection**: Crawl the target website and collect all URLs from sitemap
2. **Content Extraction**: Extract text content from each page
3. **Document Processing**: Convert pages into structured documents/chunks
4. **Embedding Generation**: Transform documents into vector embeddings using an embedding model
5. **Semantic Index**: Build a searchable semantic index from vectors
6. **Knowledge Base Storage**: Store embeddings and metadata in a vector database

### Phase 2: Query & Response (Runtime)
1. **User Question**: User submits a natural language question
2. **Query Embedding**: Convert the question into a vector embedding using the same embedding model
3. **Semantic Search**: Perform similarity search in the knowledge base
4. **Ranked Results**: Retrieve the most relevant document chunks
5. **LLM Response**: Feed ranked results + user question to LLM for answer generation
6. **Response Delivery**: Return the generated answer to the user

## Key Components

- **Sitemap Crawler**: Extracts all URLs from website sitemap
- **Embedding Model**: Converts text to vector representations (e.g., sentence-transformers, OpenAI embeddings)
- **Vector Database**: Stores and enables semantic search (e.g., FAISS, Pinecone, ChromaDB)
- **LLM**: Generates natural language responses (e.g., GPT, Claude, Llama)
- **Semantic Search Engine**: Finds relevant content based on query similarity

## Technologies (Planned)
- Python
- LangChain / LlamaIndex (RAG framework)
- Vector Database (FAISS/ChromaDB/Pinecone)
- Embedding Model (OpenAI/HuggingFace)
- LLM API (OpenAI/Anthropic/Local models)

## Getting Started
Coming soon...

## License
See LICENSE file for details.
