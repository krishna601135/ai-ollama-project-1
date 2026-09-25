from typing import Optional
from bson import ObjectId


class Conversation:
    def __init__(
        self,
        user_id: ObjectId,
        title: str,
        _id: Optional[ObjectId] = None
    ):
        self.id = _id
        self.user_id = user_id
        self.title = title

    def to_document(self):
        return{
            "user_id": self.user_id,
            "title": self.title
        }