from typing import Any
from openai import OpenAI
from models.dataclasses.LLLMConfig import LLMConfig

class LLMProvider:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = OpenAI(base_url=config.base_url, api_key=config.api_key)

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None):
        return self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else None,
        )