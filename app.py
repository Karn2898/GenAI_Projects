import chainlit as cl

from src.llm import generate_llm_reply
from src.prompt import build_system_prompt, generate_reply


@cl.on_message
async def main(message: cl.Message) -> None:
    system_prompt = build_system_prompt()
    llm_reply = generate_llm_reply(message.content, system_prompt=system_prompt)

    fallback_markers = (
        "LLM API key is missing",
        "Could not reach the LLM endpoint",
        "LLM request failed",
        "Something went wrong while calling the LLM",
        "The LLM returned no response",
        "The LLM response was empty",
    )

    if llm_reply.startswith(fallback_markers):
        rule_based = generate_reply(message.content)
        reply = f"{llm_reply}\n\nFallback suggestion:\n{rule_based}"
    else:
        reply = llm_reply

    await cl.Message(content=reply).send()