from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


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
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    post = post.dict()
    post['id'] = randrange(0,10000000)
    posts.append(post)
    return {"data": post}



@app.get("/posts/latest")
async def get_last_post():
    data = posts[len(posts)-1]
    return {"data": data}


@app.get("/posts/{id}")
async def get_post(id:int, response:Response):
    # Find post
    data = find_post(id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return {"data": data}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    deleted = delete_post_by_id(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id:int, post:Post):
    post_to_update = find_post(id)
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    # delete and create
    delete_post_by_id(id)
    post = post.dict()
    post['id'] = id
    posts.append(post)
    print(posts)
    return {"data": post}