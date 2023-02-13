from pydantic import BaseModel


class PostAdd(BaseModel):
    title: str
    text: str
