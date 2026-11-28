from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str
    users_added_context: str = ""

class ChatResponse(BaseModel):
    session_id: str
    reply: str