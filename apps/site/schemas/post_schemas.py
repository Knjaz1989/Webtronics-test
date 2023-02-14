from typing import Optional

from pydantic import BaseModel, Field


class PostAdd(BaseModel):
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class PostUpdate(BaseModel):
    post_id: int = Field(..., ge=1)
    title: str = Field(None, min_length=1)
    text: str = Field(None, min_length=1)


class PostDelete(BaseModel):
    post_id: int = Field(..., ge=1)
