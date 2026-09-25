from pydantic import BaseModel

class MessageCreate(BaseModel):
    conversation_id: str
    message: str