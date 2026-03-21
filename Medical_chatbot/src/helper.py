from pathlib import Path
from typing import List, Optional

try:
    from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
except ImportError:
    from langchain.document_loaders import PyPDFLoader, DirectoryLoader

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:  
    from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings


def load_pdf_file(data: str) -> List:
    """Load all PDF documents from a directory."""
    data_path = Path(data)

    if not data_path.exists():
        raise FileNotFoundError(f"Directory not found: {data_path}")
    if not data_path.is_dir():
        raise NotADirectoryError(f"Expected a directory path, got: {data_path}")

    loader = DirectoryLoader(
        str(data_path),
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )
    return loader.load()


def text_split(extracted_data: List, chunk_size: int = 500, chunk_overlap: int = 20) -> List:
    """Split documents into chunks for embedding/vector storage."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and < chunk_size")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_documents(extracted_data)


def download_hugging_face_embeddings(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs: Optional[dict] = None,
    encode_kwargs: Optional[dict] = None,
):
    """Initialize and return HuggingFace embeddings model."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs or {"device": "cpu"},
        encode_kwargs=encode_kwargs or {"normalize_embeddings": True},
    )