from models.conversation_storage.ConversationStore import ConversationStore
from services.LLMProvider import LLMProvider
from services.ToolRegistry import ToolRegistry

class AgentService:
    def __init__(self, provider: LLMProvider, tools: ToolRegistry, store: ConversationStore):
        self.provider = provider
        self.tools = tools
        self.store = store

    def run_turn(self, session_id: str, user_message: str, active_note: str = "") -> str:
        system_prompt = (
            "You are a D&D Game Master assistant. Use tools to check campaign notes "
            "or D&D rules before inventing established lore.\n"
            f"Currently open note:\n{active_note[:800]}"
        )
        self.store.append(session_id, {"role": "user", "content": user_message})

        for _ in range(5):
            history = self.store.get_window(session_id, self.provider.config.max_history_messages)
            messages = [{"role": "system", "content": system_prompt}, *history]

            response = self.provider.complete(messages, self.tools.schemas)
            msg = response.choices[0].message
            self.store.append(session_id, msg.model_dump(exclude_none=True))

            if not msg.tool_calls:
                return msg.content or ""

            for call in msg.tool_calls:
                output = self.tools.execute(call.function.name, call.function.arguments)
                self.store.append(
                    session_id,
                    {"role": "tool", "tool_call_id": call.id, "content": output},
                )

        return "Stopped: exceeded maximum tool-calling steps."