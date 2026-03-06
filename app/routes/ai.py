from fastapi import APIRouter,Depends
from app.services.ai_services import ask_ai_about_note_service
from app.schemas.ai_schema import AIRequest
from app.models import User
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user_optional

router=APIRouter(prefix="/ai",tags=["AI"])

@router.post("/ask")
def ask_ai_about_note(request:AIRequest,db:Session=Depends(get_db),current_user:User|None=Depends(get_current_user_optional)):
    answer=ask_ai_about_note_service(request,db,current_user)
    return{
        "answer":answer
        }