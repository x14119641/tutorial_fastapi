
from fastapi import FastAPI
from .routes import hello, user, post, auth, vote


app = FastAPI()

app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)