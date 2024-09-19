from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime




class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # raiting: Optional[int] = None
    
class PostCreate(PostBase):
    pass


class Post(PostBase):
    id:int
    created_at:datetime
    
    
class UserBase(BaseModel):
    id:int
    username: str
    email:EmailStr
    disabled: bool | None = None
    
    
class User(UserBase):
    id:int
    username: str
    email:EmailStr
    created_at:datetime
    
    
class UserCreate(UserBase):
    password:str


class UserLogin(UserBase):
    username: str | EmailStr
    password:str
    
    
class UserResponse(BaseModel):
    id:int
    username: str
    email:EmailStr
    created_at:datetime
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    
    
    
