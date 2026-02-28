from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.core.security import decode_access_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/authorization/login")

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
