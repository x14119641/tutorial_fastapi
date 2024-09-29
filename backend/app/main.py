
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import hello, user, post, auth, vote


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://127.0.0.1",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8080",
    "http://192.168.16.168:8080",
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
