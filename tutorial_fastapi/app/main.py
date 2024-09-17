from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from typing import List, Annotated
from .schema import (Post, PostCreate, User, UserCreate, UserResponse,
                     Token, TokenData)
from .database import DatabaseAsync
from .config import Settings
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt 



async def get_user(username: str):
    data = await db.fetchone("SELECT * FROM users WHERE username = ($1)", (username,))
    print('User: ', data)
    if data:
        return UserCreate(**data)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()

app = FastAPI()
settings = Settings.read_file()
secrets = Settings.read_file('tutorial_fastapi/app/secrets.json')

db = DatabaseAsync(**settings)


def verify_password(plain_password, hashed_password):
    verify = password_hash.verify(plain_password, hashed_password)
    # print('verified: ', verify, ' Pwd plain: ', plain_password, 'hashed pwd: ', hashed_password)
    return verify

def get_password_hash(password):
    return password_hash.hash(password)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire =  datetime.now(timezone.utc) + expires_delta
    else:
        expire =  datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secrets["SECRET_KEY"], algorithm=secrets["ALGORITHM"])
    return encoded_jwt
        


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secrets["SECRET_KEY"], algorithms=[secrets["ALGORITHM"],])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/")
async def get_root():
    return {"data": "Hello World!"}


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=secrets["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@app.get("/posts", response_model=List[Post,])
async def get_posts():
    rows = await db.fetchall("SELECT * FROM posts")
    return rows


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post:PostCreate):
    row = await db.execute_and_get_record(
        "INSERT INTO posts (title, content, published) VALUES ($1, $2, $3)", 
        (post.title, post.content, str(post.published)))
    data = await db.fetchone("SELECT * FROM posts WHERE id = ($1)", (row['id'],))
    return data



@app.get("/posts/latest", response_model=Post)
async def get_last_post():
    rows = await db.fetchone("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    return rows


@app.get("/posts/{id}", response_model=Post)
async def get_post(id:int, response:Response):
    # Find post
    rows = await db.fetchone("SELECT * FROM posts WHERE id=($1)", (id,))
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return rows



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    row = await db.execute_and_get_record("DELETE FROM posts WHERE  id=($1)", (id,))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
async def update_post(id:int, post:PostCreate):
    row = await db.execute_and_get_record(
        "UPDATE posts SET title=($1), content=($2), published=($3) WHERE id=($4)", 
        (post.title, post.content, str(post.published),id,))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return row


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user:UserCreate):
    # Check if email exists
    email_exists = await db.fetchone("SELECT email FROM users WHERE email=($1)", (user.email,))
    if email_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email already registered.')
    
    # Check if email exists
    username_exists = await db.fetchone("SELECT username FROM users WHERE username=($1)", (user.username,))
    if email_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User already registered.')
    
    hashed_pwd = password_hash.hash(user.password)
    
    row = await db.execute_and_get_record(
        "INSERT INTO users (username, email, password) VALUES ($1, $2, $3)", 
        (user.username, user.email, hashed_pwd,))
    data = await db.fetchone("SELECT * FROM users WHERE id = ($1)", (row['id'],))
    return data