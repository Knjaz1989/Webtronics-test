from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, EmailStr, Field

from settings import config


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserBase):
    """Log in request schema.
    Email and password inherits from parent"""
    expire_minutes: int = Field(config.TOKEN_EXPIRE_MINUTES, ge=1)

    @validator('email')
    def lowerify_email(cls, value):
        """To lowercase"""
        return value.lower()


class UserCreate(UserBase):
    """Sign up request schema
    Email and password inherits from parent"""
    name: str


class TokenResponse(BaseModel):
    """Response schema with token details."""
    access_token: str
    expires: datetime
    token_type: Optional[str] = 'Bearer'
