
from fastapi import FastAPI
from .routes import hello, user, post, auth


app = FastAPI()

app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)