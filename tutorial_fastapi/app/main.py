from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from .schema import Post, PostCreate
from .database import DatabaseAsync
from .config import Settings

app = FastAPI()
settings = Settings.read_file()

db = DatabaseAsync(**settings)


@app.get("/")
async def get_root():
    return {"data": "Hello World!"}


@app.get("/posts")
async def get_posts():
    rows = await db.fetchall("SELECT * FROM posts")
    return {"data": rows}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post:PostCreate):
    rows = await db.execute_and_get_record(
        "INSERT INTO posts (title, content, published) VALUES ($1, $2, $3)", 
        (post.title, post.content, str(post.published)))
    #rows = await db.fetchone("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    return {"data": rows}



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
    row = await db.execute_and_get_record("DELETE FROM posts WHERE  id=($1)", (id,))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id:int, post:PostCreate):
    row = await db.execute_and_get_record(
        "UPDATE posts SET title=($1), content=($2), published=($3) WHERE id=($4)", 
        (post.title, post.content, str(post.published),id,))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return {"data": row}