from __future__ import annotations


SYSTEM_PROMPT = (
	"You are ZomatoBot, a food discovery assistant. "
	"Be concise, friendly, and helpful."
)


def build_system_prompt() -> str:
	return SYSTEM_PROMPT


def generate_reply(user_message: str) -> str:
	"""Return a simple rule-based reply for the current user message."""
	text = (user_message or "").strip()
	if not text:
		return "Tell me what you're craving and your area, and I'll suggest options."

	lowered = text.lower()

	if any(greet in lowered for greet in ["hi", "hello", "hey"]):
		return (
			"Hi! I can help you find food quickly. "
			"Share your city/area, cuisine, and budget (for example: 'Bandra, pizza, under 500')."
		)

	if "cheap" in lowered or "budget" in lowered or "under" in lowered:
		return (
			"Got it. For budget picks, tell me your exact area and cuisine. "
			"I can suggest options under your target amount."
		)

	if "near" in lowered or "nearby" in lowered or "around" in lowered:
		return "Share your location pin/area name and cuisine preference, and I'll narrow it down."

	if "recommend" in lowered or "suggest" in lowered or "best" in lowered:
		return (
			"Happy to recommend. Please share location, cuisine, and budget so I can give relevant options."
		)

	return (
		"I can help with restaurant discovery, cuisine suggestions, and budget-friendly picks. "
		"Tell me your location, cuisine, and budget."
	)
