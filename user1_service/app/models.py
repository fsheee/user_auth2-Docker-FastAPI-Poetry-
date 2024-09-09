from fastapi import Form
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Annotated, Optional


class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str


class Register_User(BaseModel):
    username: Annotated[
        str,
        Form()]
    
    email: Annotated[
        str,
        Form()]
    
    password: Annotated[
        str,
        Form()]

class UserResponse(SQLModel):
    user_id: int
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(SQLModel):
    username: Optional[str] = None


class RefreshTokenData(SQLModel):
    email: str



