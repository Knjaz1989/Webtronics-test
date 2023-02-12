from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, EmailStr, UUID4, Field


class UserLogin(BaseModel):
    """Log in request schema."""
    email: EmailStr
    password: str

    @validator('email')
    def lowerlify_email(cls, value):
        """To lowercase"""
        return value.lower()


class UserCreate(UserLogin):
    """
    Sign up request schema.
    Email and password inherit from parent
    """
    name: str


class TokenResponse(BaseModel):
    """Response schema with token details."""
    token: UUID4 = Field(..., alias='access_token')
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @validator('token')
    def hexlify_token(cls, value):
        """UUID to hex string converter."""
        return value.hex
