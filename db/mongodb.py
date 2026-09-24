from pymongo import MongoClient
from config.settings import MONGO_URI


client = MongoClient()
db = client['ai_chatbot']