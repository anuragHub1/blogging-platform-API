from datetime import datetime
from pydantic import BaseModel
from typing import List

class CreatePost(BaseModel):
    title: str
    content: str
    category: str
    tags: str

class UpdatePost(BaseModel):
    title:str
    content:str
    category:str
    tags:str

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    tags:List[str]
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes=True