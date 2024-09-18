from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..schema import (User, UserCreate, UserResponse,
                      Post, PostCreate)
from ..dependencies import db, password_hash
from typing import List, Annotated


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[Post,])
async def get_posts():
    rows = await db.fetchall("SELECT * FROM posts")
    return rows


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post:PostCreate):
    row = await db.execute_and_get_record(
        "INSERT INTO posts (title, content, published) VALUES ($1, $2, $3)", 
        (post.title, post.content, str(post.published)))
    data = await db.fetchone("SELECT * FROM posts WHERE id = ($1)", (row['id'],))
    return data



@router.get("/latest", response_model=Post)
async def get_last_post():
    rows = await db.fetchone("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    return rows


@router.get("/{id}", response_model=Post)
async def get_post(id:int, response:Response):
    # Find post
    rows = await db.fetchone("SELECT * FROM posts WHERE id=($1)", (id,))
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return rows



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    row = await db.execute_and_get_record("DELETE FROM posts WHERE id=($1)", (id,))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
async def update_post(id:int, post:PostCreate):
    row = await db.execute_and_get_record(
        "UPDATE posts SET title=($1), content=($2), published=($3) WHERE id=($4)", 
        (post.title, post.content, str(post.published),id,))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return row