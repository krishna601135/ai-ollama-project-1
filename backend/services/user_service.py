from fastapi import HTTPException
import bcrypt

from db.mongodb import users_collection
from models.user import User


def create_user(name: str, email: str, password: str):

    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    user = User(
        name=name,
        email=email,
        password_hash=password_hash
    )

    result = users_collection.insert_one(
        user.to_document()
    )

    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email
    }


def get_user_by_email(email: str):
    user_document = users_collection.find_one({"email": email})
    if not user_document:
        return None 
    return User(
        _id=user_document["_id"],
        name=user_document["name"],
        email=user_document["email"],
        password_hash=user_document["password_hash"]
    )


