from pydantic import BaseModel, Field


class PostAdd(BaseModel):
    title: str
    text: str


class PostDelete(BaseModel):
    post_id: int = Field(..., ge=1)
