from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError

from settings import config


def create_token(data: dict) -> tuple:
    """Create token for user"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=to_encode.get("expire_minutes")
    )
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET, algorithm=config.ALGORITHM
    )
    return encoded_jwt, expire


def decode_token(token: str) -> dict | str:
    try:
        data = jwt.decode(token, config.SECRET, algorithms=[config.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong token or it has expired",
        )
    return data

