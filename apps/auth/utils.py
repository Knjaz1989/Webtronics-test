from datetime import datetime, timedelta
import requests

from jose import jwt

from apps.main_helpers import get_hash_password
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
