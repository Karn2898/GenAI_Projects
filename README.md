# Zomato Chatbot

A Chainlit-based food discovery assistant that uses an OpenAI-compatible LLM endpoint, with a rule-based fallback when the LLM call fails.

## Features

- Chat interface powered by Chainlit
- OpenAI-compatible chat completions integration
- Configurable model and base URL through environment variables
- Graceful fallback to deterministic rule-based suggestions

## Project Structure

app.py: Chainlit app entrypoint
src/llm.py: OpenAI-compatible LLM client
src/prompt.py: system prompt and rule-based fallback responses
requirements.txt: runtime dependencies

## Requirements

- Python 3.10+
- Internet access for LLM API calls
- API key for an OpenAI-compatible provider

## Setup

1. Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a .env file in the project root.

```env
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1
LLM_TIMEOUT_SECONDS=25
```

Notes:
- You can also use OPENAI_API_KEY instead of LLM_API_KEY.
- LLM_BASE_URL is for any OpenAI-compatible endpoint.

## Run

```bash
chainlit run app.py
```

Then open the local URL shown by Chainlit (usually http://localhost:8000).

## Behavior

- If LLM configuration and network are healthy, responses come from the configured model.
- If the LLM request fails, the chatbot returns an error summary and a rule-based fallback suggestion.

## Troubleshooting

- Missing API key: set LLM_API_KEY (or OPENAI_API_KEY) in .env.
- Connection issue: verify internet access and LLM_BASE_URL.
- Empty model response: retry with a clearer prompt.

## Useful Commands

```bash
chainlit run app.py
python app.py
```

## License

See LICENSE.