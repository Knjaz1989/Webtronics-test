from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, EmailStr, UUID4, Field


class UserCreate(BaseModel):
    name: str
    password: str
    email: EmailStr


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias='access_token')
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @validator('token')
    def hexlify_token(cls, value):
        """UUID to hex string converter."""
        return value.hex


class Post(BaseModel):
    title: str
    text: str
