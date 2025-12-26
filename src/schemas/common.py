from pydantic import BaseModel
from typing import Optional

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