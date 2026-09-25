from fastapi import APIRouter, Header, HTTPException

from schemas.user import UserCreate, UserLogin
from services.user_service import create_user
from services.auth_service import login_user, get_user_id_from_token 


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register_user(user: UserCreate):

    return create_user(
        user.name,
        user.email,
        user.password
    )

@router.post("/login")
def login(user: UserLogin):

    return login_user(
        user.email,
        user.password
    )


@router.get('/me')
def get_current_user(
    authorization: str = Header(...)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]
    print("token+++++++++++++++++++++++++", token)
    user_id = get_user_id_from_token(token)

    return {
        "user_id": user_id
    }
    