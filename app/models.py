from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, table
from sqlalchemy import Column, DateTime, text

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})
    created: Optional[datetime] = Field(default= None, sa_column = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False))
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)
    user: Optional["User"] = Relationship()

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created: Optional[datetime] = Field(default= None, sa_column = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False))

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    post_id: int = Field(primary_key=True, foreign_key="posts.id", ondelete="CASCADE")
    user_id: int = Field(primary_key=True, foreign_key="users.id", ondelete="CASCADE")
