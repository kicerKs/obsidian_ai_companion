from dataclasses import dataclass
import os

@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    api_key: str
    model: str
    max_history_messages: int = 14

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls(
            base_url=os.environ["LLM_BASE_URL"],
            api_key=os.environ["LLM_API_KEY"],
            model=os.environ["LLM_MODEL"],
            max_history_messages=int(os.getenv("LLM_MAX_HISTORY", "14")),
        )