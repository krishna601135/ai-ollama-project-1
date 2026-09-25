import json
import requests

from fastapi import HTTPException
from db.mongodb import db
from config.settings import OLLAMA_URL, OLLAMA_MODEL
from models.message import Message
from bson import ObjectId

from db.mongodb import messages_collection
from db.mongodb import conversations_collection

messages = db["messages"]


def save_message(conversation_id, role, content):
    message = Message(
    conversation_id=conversation_id,
    role="user",
    content="What is Python?"
    )
    message.to_document()

    return messages.insert_one(message)


def get_messages(conversation_id):
    return list(
        messages.find(
            {"conversation_id": conversation_id}
        ).sort("_id", 1)
    )


# def ask_ollama(conversation_id):

#     history = get_messages(conversation_id)

#     ollama_messages = []

#     for message in history:
#         ollama_messages.append({
#             "role": message["role"],
#             "content": message["content"]
#         })

#     response = requests.post(
#         f"{OLLAMA_URL}/api/chat",
#         json={
#             "model": OLLAMA_MODEL,
#             "messages": ollama_messages,
#             "stream": True
#         },
#         stream=True
#     )

#     assistant_message = ""

#     print("AI: ", end="", flush=True)

#     for line in response.iter_lines():

#         if line:

#             chunk = json.loads(line)

#             content = chunk["message"]["content"]

#             print(content, end="", flush=True)

#             assistant_message += content

#     print()

#     save_message(
#         conversation_id,
#         "assistant",
#         assistant_message
#     )

#     return assistant_message



def get_conversation_messages(conversation_id: str,  user_id: str):
    conversation = conversations_collection.find_one({
        "_id": ObjectId(conversation_id),
        "user_id": user_id
    })

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = messages_collection.find({
        "conversation_id": ObjectId(conversation_id)
    }).sort("_id", 1)

    return [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in messages
    ]


def send_message(
    conversation_id: str,
    user_id: str,
    message: str
):
    # Check conversation belongs to user
    conversation = conversations_collection.find_one({
        "_id": ObjectId(conversation_id),
        "user_id": user_id
    })

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # Save user message
    user_message = Message(
        conversation_id=ObjectId(conversation_id),
        role="user",
        content=message
    )

    messages_collection.insert_one(
        user_message.to_document()
    )

    # Get previous messages
    messages = get_conversation_messages(
        conversation_id,
        user_id
    )

    # Send messages to Ollama
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    assistant_content = data["message"]["content"]

    # Save assistant message
    assistant_message = Message(
        conversation_id=ObjectId(conversation_id),
        role="assistant",
        content=assistant_content
    )

    messages_collection.insert_one(
        assistant_message.to_document()
    )

    # Return AI response
    return {
        "role": "assistant",
        "content": assistant_content
    }