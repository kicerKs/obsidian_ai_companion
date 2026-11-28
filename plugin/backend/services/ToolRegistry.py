import json
from typing import Any, Callable

class ToolRegistry:
    def __init__(self):
        self._schemas: list[dict[str, Any]] = []
        self._handlers: dict[str, Callable[..., str]] = {}

    def register(self, schema: dict[str, Any], fn: Callable[..., str]) -> None:
        self._schemas.append(schema)
        self._handlers[schema["function"]["name"]] = fn

    @property
    def schemas(self) -> list[dict[str, Any]]:
        return self._schemas

    def execute(self, name: str, arguments_json: str) -> str:
        if name not in self._handlers:
            return f"Error: Unknown tool '{name}'"
        try:
            args = json.loads(arguments_json) if arguments_json else {}
            return str(self._handlers[name](**args))
        except Exception as e:
            return f"Tool execution error: {e}"