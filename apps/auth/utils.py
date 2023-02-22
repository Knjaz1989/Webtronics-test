from datetime import datetime, timedelta
import hashlib
import requests

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


def get_hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hash_pass


def validate_password(password: str, hashed_password: str):
    """Validate password hash with db hash."""
    return get_hash_password(password) == hashed_password



def verify_email(email: str) -> str | None:
    url = 'https://api.hunter.io/v2/email-verifier'
    params = {'email': email, 'api_key': config.HUNTER_API_KEY}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('data').get('status') == 'valid':
            return 'valid'