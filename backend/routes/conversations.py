from fastapi import APIRouter, Header, HTTPException

from schemas.conversation import ConversationCreate
from services.conversation_service import create_conversation, get_user_conversations
from services.auth_service import get_user_id_from_token


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post("/")
def create_new_conversation(
    conversation: ConversationCreate,
    authorization: str = Header(...)
):
    if not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=401,
            detail='Invalid authorization header'
        )

    token = authorization.split(" ")[1]

    user_id = get_user_id_from_token(token)

    return create_conversation(
        user_id,
        conversation.title
    )


@router.get("/")
def get_conversations(
    authorization: str = Header(...)
):
    if not authorization.startswith('Bearer '):
            raise HTTPException(
                status_code=401,
                detail='Invalid authorization header'
            )

    token = authorization.split(" ")[1]
    user_id = get_user_id_from_token(token)
    print("userid++++++++++++++", user_id)
    return get_user_conversations(user_id)
    
