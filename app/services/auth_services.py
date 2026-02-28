from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.auth_schema import UserCreate
from app.core.security import hash_password,verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

def register_user_service(user:UserCreate,db:Session):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=406,detail="User with this email already exists")
    user=User(name=user.name,
              email=user.email,
              password_hash=hash_password(user.password))
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login_user_service(form_data:OAuth2PasswordRequestForm,db:Session):
    user=db.query(User).filter(User.email==form_data.username).first()
    if not user or not verify_password(form_data.password,user.password_hash):
        raise HTTPException(status_code=401,
                            detail="Invalid credentials")
    
    access_token=create_access_token(
        data={
            "sub":str(user.id)
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }