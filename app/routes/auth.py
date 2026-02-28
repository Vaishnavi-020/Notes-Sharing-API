from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.services.auth_services import register_user_service,login_user_service
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.auth_schema import UserCreate,UserResponse,Token,UserOut
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(prefix='/authorization',tags=["Authorization"])

@router.post('/register',response_model=UserResponse,status_code=201)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    return register_user_service(user,db)

@router.post('/login',response_model=Token)
def login_user(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return login_user_service(form_data,db)

@router.get("/me",response_model=UserOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user
