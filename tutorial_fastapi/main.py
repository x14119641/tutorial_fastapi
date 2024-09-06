from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def get_root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"message": "Posts data"}


@app.post("/createposts")
async def create_post(payLoad:dict=Body(...)):
    return {"message": f"Title : {payLoad['title']}, Content: {payLoad['content']}"}