from flask import Flask , render_template , request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_nvidia_ai_endpoints import ChatNVIDIA
try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import system_prompt
import os
from pathlib import Path

app = Flask(__name__)

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not PINECONE_API_KEY or not NVIDIA_API_KEY:
    raise ValueError(
        "Missing API keys. Add PINECONE_API_KEY and NVIDIA_API_KEY to .env in the project root."
    )

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["NVIDIA_API_KEY"] = NVIDIA_API_KEY

embeddings = download_hugging_face_embeddings()
index_name = os.getenv("PINECONE_INDEX_NAME", "medicalbot")
startup_error = None
retriever = None

try:
    docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
except Exception as exc:
    startup_error = (
        f"Pinecone index '{index_name}' is unavailable. "
        "Run store_index.py to create/populate it, then restart the app. "
        f"Details: {exc}"
    )
    print(startup_error)


llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    api_key=NVIDIA_API_KEY,
    temperature=0.4,
    max_tokens=500,
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
]
)

question_answering_chain = create_stuff_documents_chain(llm , prompt)
rag_chain = create_retrieval_chain(retriever, question_answering_chain) if retriever else None

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    if rag_chain is None:
        return startup_error or "RAG chain is not initialized. Check Pinecone index setup."

    msg = request.form["msg"]
    print(msg)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host ="0.0.0.0", port =8080)