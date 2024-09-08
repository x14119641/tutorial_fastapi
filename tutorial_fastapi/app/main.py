from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from .database import DatabaseAsync

HOST = '127.0.0.1'
USER = 'postgres'
PWD = 'postgres'
DB = 'tutorial_fastapi'


app = FastAPI()
db = DatabaseAsync(host=HOST, user=USER, password=PWD, database=DB)
print(db)

# mocking db
global posts 
posts = [{"bla":"blo", "id":1}, {"bla":"blo", "id":2}]




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    raiting: Optional[int] = None
    


def find_post(id:int):
    return next((item for item in posts if item['id'] == id), None)


def delete_post_by_id(id:int):
    initial_len_posts = len(posts)
    posts[:] = [item for item in posts if item.get('id') != id]
    if initial_len_posts == len(posts):
        return False
    return True


@app.get("/")
async def get_root():
    return {"data": "Hello World!"}


@app.get("/posts")
async def get_posts():
    rows = await db.fetchall("SELECT * FROM posts")
    return {"data": rows}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    await db.execute(
        "INSERT INTO posts (title, content, published) VALUES ($1, $2, $3)", 
        (post.title, post.content, str(post.published)))
    return {"data": post}



@app.get("/posts/latest")
async def get_last_post():
    rows = await db.fetchone("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    return {"data": rows}


@app.get("/posts/{id}")
async def get_post(id:int, response:Response):
    # Find post
    rows = await db.fetchone("SELECT * FROM posts WHERE id=($1)", (id,))
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return {"data": rows}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    post_exist = await db.fetchone("SELECT * FROM posts WHERE id=($1)", (id,))
    await db.execute("DELETE FROM posts WHERE  id=($1)", (id,))
    if post_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id:int, post:Post):
    post_to_update = await db.fetchone("SELECT * FROM posts WHERE id=($1)", (id,))
    await db.execute(
        "UPDATE posts SET title=($1), content=($2), published=($3) WHERE id=($4)", 
        (post.title, post.content, str(post.published),id,))
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return {"data": post}