from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    raiting: Optional[int] = None
    
class PostCreate(Post):
    pass