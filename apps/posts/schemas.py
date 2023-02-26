from enum import Enum
from typing import List

from pydantic import BaseModel, Field, root_validator, Extra


class EnumAction(Enum):
    like = 'like'
    dislike = 'dislike'


class PostAdd(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class PostDataResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        # Don't show extra fields
        extra = Extra.ignore
        # Can convert a database model to a pydantic model using 'from_orm'
        # method
        orm_mode = True


class BaseResponse(BaseModel):
    detail: str


class PostAddGetResponse(BaseResponse):
    """Inherit 'detail' field from parent"""
    data: PostDataResponse


class PostGetAllResponse(BaseResponse):
    data: List[PostDataResponse]


class PostBase(BaseModel):
    id: int = Field(..., ge=1, alias="post_id")


class PostRate(PostBase):
    """Inherit 'id' field from parent"""
    action: EnumAction


class PostSearch(BaseModel):
    title: str = Field(None, min_length=1)
    content: str = Field(None, min_length=1)

    @root_validator()
    def check_fields(cls, values):
        if not values.get('title') and not values.get('content'):
            raise ValueError(
                "Expected two fields or one of 'title' or 'context'")
        return values


class PostUpdate(PostBase, PostSearch):
    """Inherit 'id' field from PostBase.
    Inherit 'title' and 'content' fields and validation from PostSearch"""
