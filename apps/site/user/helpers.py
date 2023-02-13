import hashlib
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError

from .schemas import UserCreate
from database.db_connection import db
from settings import config


def hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hash_pass


def validate_password(password: str, hashed_password: str):
    """Validate password hash with db hash."""
    return hash_password(password) == hashed_password


def create_token(data: dict) -> tuple:
    """Create token for user"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=to_encode.get("expire_minutes")
    )
    to_encode.update({"exp": expire})
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
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data


async def create_user(user: UserCreate):
    """Create new user."""
    hashed_password = hash_password(user.password)
    query = """
        INSERT INTO users VALUES (DEFAULT, :name, :password, :email)
        """
    await db.execute(
        query,
        {
            'name': user.name,
            'password': hashed_password,
            'email': user.email
        }
    )
    return {"status": "Success", "msg": "The user was created successfully"}


async def get_user_by_email(email: str):
    """Return user info by email."""
    query = """
        SELECT * FROM users
        WHERE email = :email
        """
    user = await db.fetch_one(query, {'email': email})
    return dict(user._mapping)
