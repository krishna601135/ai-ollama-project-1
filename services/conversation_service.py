from db.mongodb import db

conversations = db["conversations"]


def create_conversation(user_id, title):
    conversation = {
        "user_id": user_id,
        "title": title
    }

    result = conversations.insert_one(conversation)

    return conversations.find_one({
        "_id": result.inserted_id
    })