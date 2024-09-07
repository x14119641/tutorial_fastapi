from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    raiting: Optional[int] = None
    
    
@app.get("/")
async def get_root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"message": "Posts data"}


@app.post("/createposts")
async def create_post(post:Post):
    return {"data": post}