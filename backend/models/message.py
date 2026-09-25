from typing import Optional
from bson import ObjectId


class Message:
    def __init__(
        self,
        conversation_id: ObjectId,
        role: str,
        content: str,
        _id: Optional[ObjectId] = None
    ):
        self.id = _id
        self.conversation_id = conversation_id
        self.role = role
        self.content = content

    def to_document(self):
        return {
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content
        }