import hashlib
from datetime import datetime, timedelta
from sqlalchemy import and_

from apps.site.schemas.users import UserCreate
from database.db_connection import db
from database.models import User, Token


def hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hash_pass


def validate_password(password: str, hashed_password: str):
    """Validate password hash with db hash."""
    return hash_password(password) == hashed_password


async def create_user_token(user_id: int):
    """Create token for user with user_id."""
    query = (
        Token.insert()
        .values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
        .returning(Token.token, Token.expires)
    )
    return await db.fetch_one(query)


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
    return await db.fetch_one(query, {'email': email})


async def get_user_by_token(token: str):
    """Return user info by token."""
    query = Token.join(User).select().where(
        and_(
            Token.token == token,
            Token.expires > datetime.now()
        )
    )
    return await db.fetch_one(query)
