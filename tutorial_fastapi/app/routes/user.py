from fastapi import APIRouter, Depends, status, HTTPException
from ..schema import User, UserCreate, UserResponse
from ..dependencies import db, oauth2_scheme, password_hash
from .auth import get_current_active_user
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/hello", response_model=UserResponse)
async def read_hello():
    rows = await db.fetchone("SELECT * FROM users WHERE id=3 LIMIT 1")
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return rows


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],):
    return current_user

@router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(id:int, 
                         dependencies:Annotated[UserResponse, Depends(get_current_active_user)]):
    # Find user
    rows = await db.fetchone("SELECT * FROM users WHERE id=($1) LIMIT 1", (id,))
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found ')
    return rows

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
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