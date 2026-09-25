from typing import Optional
from bson import ObjectId


class User:
    def __init__(
        self,
        name: str,
        email: str,
        password_hash: str,
        _id: Optional[ObjectId] = None
    ):
        self.id = _id
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def to_document(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash
        }