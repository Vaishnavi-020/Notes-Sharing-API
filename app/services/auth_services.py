from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.auth_schema import UserCreate
from app.core.security import hash_password

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