from db.mongodb import db

users = db['users']


def get_or_create_user(email, name):
    user = user.find_one({"email": email})
    if user:
        return user

    user = {
        "name": name,
        "email": email
    }

    result = users.insert_one(user)

    return users.find_one({"_id": result.inserted_id})

