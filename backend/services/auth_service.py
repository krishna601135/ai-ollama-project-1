from datetime import timedelta, timezone, datetime

import bcrypt
import jwt 
from fastapi import HTTPException

from config.settings import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from services.user_service import get_user_by_email


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    password_hash = user.password_hash
    
    if isinstance(password_hash, str):
        password_hash = password_hash.encode("utf-8")

    password_matches = bcrypt.checkpw(password.encode('utf-8'), password_hash)
    if not password_matches:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return user

def create_access_token(user_id: str):

    expiration_time = (
        datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": user_id,
        "exp": expiration_time
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


def login_user(email: str, password: str):

    user = authenticate_user(email, password)

    access_token = create_access_token(
        str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"   
    }


def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user_id
    
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )