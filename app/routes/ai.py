from fastapi import APIRouter,Depends
from app.services.ai_services import ask_ai_about_note_service
from app.schemas.ai_schema import AIRequest
from app.models import User
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user_optional

router=APIRouter(prefix="/ai",tags=["AI"])

@router.post("/ask/{note_id}")
def ask_ai_about_note(note_id:int,note_data:AIRequest,db:Session=Depends(get_db),current_user:User|None=Depends(get_current_user_optional)):
    return ask_ai_about_note_service(note_id,note_data,db,current_user)