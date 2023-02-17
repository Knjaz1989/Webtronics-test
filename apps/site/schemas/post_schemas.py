from pydantic import BaseModel, Field, root_validator


class PostAdd(BaseModel):
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class PostBase(BaseModel):
    id: int = Field(..., ge=1, alias="post_id")


class PostUpdate(PostBase):
    """Inherit 'id' field from parent"""
    title: str = Field(None, min_length=1)
    text: str = Field(None, min_length=1)

    @root_validator()
    def check_fields(cls, values):
        if not values.get('title') and not values.get('text'):
            raise ValueError(
                "Expected two fields or one of 'title' or 'text'")
        return values


class PostDelete(BaseModel):
    post_id: int = Field(..., ge=1)
