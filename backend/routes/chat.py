from fastapi import APIRouter, Header, HTTPException

from services.chat_service import get_conversation_messages, send_message
from services.auth_service import get_user_id_from_token
from schemas.message import MessageCreate


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: str,
    authorization: str = Header(...)
    ):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]

    user_id = get_user_id_from_token(token)
    return get_conversation_messages(conversation_id, user_id)


@router.post("/")
def chat(
    message_data: MessageCreate,
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]

    user_id = get_user_id_from_token(token)

    return send_message(
        conversation_id=message_data.conversation_id,
        user_id=user_id,
        message=message_data.message
    )