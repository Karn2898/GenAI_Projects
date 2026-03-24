from __future__ import annotations

import json
import os
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


load_dotenv()


DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
DEFAULT_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")


def _build_messages(user_message: str, system_prompt: Optional[str] = None) -> list[dict[str, str]]:
	messages: list[dict[str, str]] = []
	if system_prompt:
		messages.append({"role": "system", "content": system_prompt})
	messages.append({"role": "user", "content": user_message})
	return messages


def generate_llm_reply(user_message: str, system_prompt: Optional[str] = None) -> str:
	"""Generate a reply from an OpenAI-compatible chat completion endpoint.

	Required env vars:
	- LLM_API_KEY (or OPENAI_API_KEY)

	Optional env vars:
	- LLM_MODEL (default: gpt-4o-mini)
	- LLM_BASE_URL (default: https://api.openai.com/v1)
	- LLM_TIMEOUT_SECONDS (default: 25)
	"""
	text = (user_message or "").strip()
	if not text:
		return "Please share your request so I can help."

	api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
	if not api_key:
		return "LLM API key is missing. Set LLM_API_KEY (or OPENAI_API_KEY) in your .env file."

	model = os.getenv("LLM_MODEL", DEFAULT_MODEL)
	base_url = os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
	timeout_seconds = float(os.getenv("LLM_TIMEOUT_SECONDS", "25"))

	payload = {
		"model": model,
		"messages": _build_messages(text, system_prompt),
		"temperature": 0.4,
	}

	request = Request(
		url=f"{base_url}/chat/completions",
		data=json.dumps(payload).encode("utf-8"),
		headers={
			"Authorization": f"Bearer {api_key}",
			"Content-Type": "application/json",
		},
		method="POST",
	)

	try:
		with urlopen(request, timeout=timeout_seconds) as response:
			body = json.loads(response.read().decode("utf-8"))
	except HTTPError as exc:
		details = exc.read().decode("utf-8", errors="ignore") if hasattr(exc, "read") else ""
		return f"LLM request failed with HTTP {exc.code}. {details[:180]}"
	except URLError:
		return "Could not reach the LLM endpoint. Check your internet and LLM_BASE_URL."
	except Exception:
		return "Something went wrong while calling the LLM. Please try again."

	choices = body.get("choices", [])
	if not choices:
		return "The LLM returned no response. Please retry with a clearer prompt."

	message = choices[0].get("message", {})
	content = (message.get("content") or "").strip()
	if not content:
		return "The LLM response was empty. Please retry."
	return content
