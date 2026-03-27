# Medical Chatbot using Flask,LangChain, Pinecone , NVIDIA NIM

<img width="1366" height="768" alt="Annotation 2026-03-21 160549" src="https://github.com/user-attachments/assets/1a52eab8-2c7b-41e9-8872-194e416af0cd" />


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

## Docker

A `dockerfile` is included in the project root. It uses a `python:3.10-slim-buster` base image, copies the application, installs dependencies, exposes port `8080`, and starts the Flask app.

```bash
docker build -t medical-chatbot .
docker run -d -p 8080:8080 \
  -e PINECONE_API_KEY=<your_key> \
  -e NVIDIA_API_KEY=<your_key> \
  -e PINECONE_INDEX_NAME=medicalbot \
  medical-chatbot
```

---

## AWS Deployment (CI/CD)

The project includes a GitHub Actions workflow (`workflows/cicd.yaml`) that automatically builds and deploys the Docker image to an AWS EC2 instance via Amazon ECR on every push to `main`.

### Architecture

```
GitHub push to main
       │
       ▼
GitHub Actions CI job
  ├── Configure AWS credentials
  ├── Log in to Amazon ECR
  ├── Create ECR repository (if absent)
  └── Build & push Docker image to ECR
       │
       ▼
GitHub Actions CD job
  ├── Configure AWS credentials
  ├── Log in to Amazon ECR
  └── SSH into EC2 → pull latest image → restart container
```

### Required GitHub Secrets

Add these secrets under **Settings → Secrets and variables → Actions** in your GitHub repository:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key ID |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret access key |
| `AWS_DEFAULT_REGION` | AWS region (e.g. `us-east-1`) |
| `ECR_REPOSITORY` | ECR repository name (e.g. `medical-chatbot`) |
| `EC2_HOST` | Public IP or hostname of your EC2 instance |
| `EC2_USERNAME` | SSH login user (e.g. `ubuntu`, `ec2-user`) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access |
| `PINECONE_API_KEY` | Pinecone API key (injected into the container) |
| `NVIDIA_API_KEY` | NVIDIA API key (injected into the container) |

### One-Time AWS Setup

> **Important:** The EC2 deployment step is skipped unless all three secrets `EC2_HOST`, `EC2_USERNAME`, and `EC2_SSH_KEY` are configured. Without them the Docker image is built and pushed to ECR but never deployed to the instance.

**1. Create an IAM user** with programmatic access and attach policies for:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonEC2FullAccess` (or a scoped policy allowing `ec2:DescribeInstances`)

**2. Launch an EC2 instance** (Ubuntu recommended):
- Open inbound port `8080` in the security group so the app is reachable from the internet.
- Install Docker on the instance:

```bash
sudo apt update && sudo apt install -y docker.io awscli
sudo usermod -aG docker $USER
# Log out and back in (or start a new session) for the group change to take effect.
```

> **Note:** The workflow passes the AWS credentials from GitHub Secrets directly to the `aws ecr get-login-password` command on the EC2 instance, so no separate `aws configure` step is required on the instance itself.

**3. Create an ECR repository** (the workflow creates it automatically if it does not exist, but you can also create it manually):

```bash
aws ecr create-repository --repository-name medical-chatbot --region <your-region>
```

### Deployment Flow

Once the secrets are configured:

1. Push any change to the `main` branch.
2. The **CI job** builds the Docker image and pushes it to ECR.
3. The **CD job** SSHs into the EC2 instance, pulls the new image, stops the old container, and starts a fresh one with all required environment variables injected.

The application will be available at:

```
http://<EC2_HOST>:8080
```

---

## Future Improvements

- Add chat history memory
- Add source citations in responses
- Add automated tests
