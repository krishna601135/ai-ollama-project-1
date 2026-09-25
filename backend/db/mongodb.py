from pymongo import MongoClient
from config.settings import MONGO_URI


client = MongoClient()
db = client['ai_chatbot']
users_collection = db["users"]
conversations_collection = db["conversations"]
messages_collection = db["messages"]