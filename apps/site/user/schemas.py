from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, EmailStr, UUID4, Field

from settings import config


class UserLogin(BaseModel):
    """Log in request schema."""
    email: EmailStr
    password: str
    expire_minutes: int = Field(config.TOKEN_EXPIRE_MINUTES, ge=1)

    @validator('email')
    def lowerify_email(cls, value):
        """To lowercase"""
        return value.lower()


class UserCreate(UserLogin):
    """Sign up request schema"""
    email: EmailStr
    password: str
    name: str


class TokenResponse(BaseModel):
    """Response schema with token details."""
    access_token: str
    expires: datetime
    token_type: Optional[str] = 'Bearer'
