from bson import ObjectId

from db.mongodb import conversations_collection
from models.conversation import Conversation


def create_conversation(user_id: str, title: str):

    conversation = Conversation(
        user_id=user_id,
        title= title
    )

    result = conversations_collection.insert_one(conversation.to_document())

    return {
        "id": str(result.inserted_id),
        "user_id": user_id,
        "title": title
    }


def get_user_conversations(user_id: str):
    conversations = conversations_collection.find({"user_id": user_id})
    return [
        {
            "id": str(conversation["_id"]),
            "title": conversation["title"]
        }
        for conversation in conversations
    ]
