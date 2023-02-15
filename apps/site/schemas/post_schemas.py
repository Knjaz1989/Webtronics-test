from typing import Dict

from pydantic import BaseModel, Field, validator, root_validator


class PostAdd(BaseModel):
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class PostUpdate(BaseModel):
    id: int = Field(..., ge=1, alias="post_id")
    title: str = Field(None, min_length=1)
    text: str = Field(None, min_length=1)

    @root_validator()
    def check(cls, values):
        if not values.get('title') and not values.get('text'):
            raise ValueError(
                "Expected two fields or one of 'title' or 'text'")
        return values


class PostDelete(BaseModel):
    post_id: int = Field(..., ge=1)
