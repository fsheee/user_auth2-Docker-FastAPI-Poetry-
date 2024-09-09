import logging

from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager

from sqlmodel import Session
from app.auth import EXPIRY_TIME, authenticate_user, create_access_token, current_user, validate_refresh_token, create_refresh_token
from app.db import get_session, create_tables
from app.models import Token, User, UserResponse
from app.router import user



async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Lifespan event started...")
    # asyncio.create_task(consume_messages('products', 'broker:19092'))
  
    create_tables()

    yield

app = FastAPI(
    lifespan=lifespan,
    title="Kafka With FastAPI User Micro Service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8006", 

            "description": "Development Server"
        }
    ]
)
app.include_router(router=user.user_router)

@app.get('/')
async def root():
    return {"message": "Micro Service  app"}


# login . username, password
@app.post('/token', response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                session:Annotated[Session, Depends(get_session)]):
    user = authenticate_user (form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    expire_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub":form_data.username}, expire_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)

    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)

@app.post("/token/refresh")
def refresh_token(old_refresh_token:str,
                  session:Annotated[Session, Depends(get_session)]):
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate":"Bearer"}
    )
    
    user = validate_refresh_token(old_refresh_token,
                                  session)
    if not user:
        raise credential_exception
    
    expire_time = timedelta(minutes=EXPIRY_TIME)
    access_token = create_access_token({"sub":user.username}, expire_time)

    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub":user.email}, refresh_expire_time)

    return Token(access_token=access_token, token_type= "bearer", refresh_token=refresh_token)




