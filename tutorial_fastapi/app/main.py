
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import hello, user, post, auth, vote


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)