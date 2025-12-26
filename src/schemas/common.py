from pydantic import BaseModel
from typing import List

class CreatePost(BaseModel):
    title: str
    content: str
    category: str
    tags: str