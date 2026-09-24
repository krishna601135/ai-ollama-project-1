import json
import requests

from db.mongodb import db
from config.settings import OLLAMA_URL, OLLAMA_MODEL

messages = db["messages"]


def save_message(conversation_id, role, content):
    message = {
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }

    return messages.insert_one(message)


def get_messages(conversation_id):
    return list(
        messages.find(
            {"conversation_id": conversation_id}
        ).sort("_id", 1)
    )


def ask_ollama(conversation_id):

    history = get_messages(conversation_id)

    ollama_messages = []

    for message in history:
        ollama_messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": ollama_messages,
            "stream": True
        },
        stream=True
    )

    assistant_message = ""

    print("AI: ", end="", flush=True)

    for line in response.iter_lines():

        if line:

            chunk = json.loads(line)

            content = chunk["message"]["content"]

            print(content, end="", flush=True)

            assistant_message += content

    print()

    save_message(
        conversation_id,
        "assistant",
        assistant_message
    )

    return assistant_message