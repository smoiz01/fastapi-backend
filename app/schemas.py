from datetime import datetime
import email
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created: datetime

    model_config = {"from_attributes": True}

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created: datetime
    user_id: int
    user: UserResponse
    votes: int
    model_config = {"from_attributes": True}

class PostListResponse(PostBase):
    id: int
    created: datetime
    user_id: int
    votes: int
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int 
    dir: Literal[0, 1]