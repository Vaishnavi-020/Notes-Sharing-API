from fastapi import APIRouter,HTTPException,Depends,UploadFile,File,Form
from sqlalchemy.orm import Session
from app.services.notes_services import create_note_service,view_my_notes_service,get_note_file_service
from app.schemas.notes_schema import NotesOut
from app.models.users import User
from app.database import get_db
from app.dependencies import get_current_user,get_current_user_optional

router=APIRouter(prefix='/notes',tags=["Notes"])

@router.post("/upload")
async def upload_note(title:str=Form(...),
                      description:str=Form(...),
                      subject:str=Form(...),
                      is_private:bool=Form(True),
                      file:UploadFile=File(...),
                      db:Session=Depends(get_db),
                      current_user=Depends(get_current_user)):
    note=create_note_service(title=title,
                                   description=description,
                                   subject=subject,
                                   is_private=is_private,
                                   file=file,
                                   db=db,
                                   current_user=current_user)
    return {
        "message":"Note Uplaoded Successfully",
        "note_id":note.id,
    }

@router.get('/my_notes',response_model=list[NotesOut])
def view_my_notes(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_my_notes_service(db,current_user)

@router.get("/{note_id}")
def get_note_file(note_id:int,db:Session=Depends(get_db),current_user:User|None=Depends(get_current_user_optional)):
    return get_note_file_service(note_id,db,current_user)