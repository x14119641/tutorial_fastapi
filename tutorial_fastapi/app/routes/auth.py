from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..schema import (Post, PostCreate, User, UserCreate, UserResponse, UserLogin,
                     Token, TokenData)
from ..dependencies import db, oauth2_scheme, password_hash, secrets
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
import jwt 

router = APIRouter(tags=["Authentcation"])


async def get_user(username: str):
    data = await db.fetchone("SELECT * FROM users WHERE username = ($1)", (username,))
    if data:
        return UserCreate(**data)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


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


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}



@router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
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

"""
@router.post("/login")
async def login(form_data:UserLogin) -> Token:
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
"""



