from fastapi import HTTPException,Depends,Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from app.core.config import SECRET_KEY,JWT_ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.core.security import decode_access_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/authorization/login")
oauth2_scheme_optional=OAuth2PasswordBearer(tokenUrl="/authorization/login",auto_error=False)

def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
):
    payload=decode_access_token(token)
    user_id:str=payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401,detail="Invalud token payload")
    user=db.query(User).filter(User.id==int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    return user

def get_current_user_optional(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme_optional)):
    if not token:
        return None
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[JWT_ALGORITHM])
        user_id:str=payload.get("sub")

        if user_id is None:
            return None
    except JWTError:
        return None
    user=db.query(User).filter(User.id==int(user_id)).first()
    return user

def pagination_params(
        page:int=Query(1,ge=1),
        limit:int=Query(10,ge=1,le=100),
):
    offset=(page-1)*limit
    return {"page":page,"limit":limit,"offset":offset}