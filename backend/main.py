from fastapi import FastAPI

from routes import users
from routes import conversations
from routes import chat



app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0"
)


app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(chat.router)


@app.get("/")
def root():

    return {
        "message": "AI Chatbot API is running"
    }