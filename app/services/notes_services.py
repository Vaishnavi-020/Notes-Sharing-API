from fastapi import HTTPException,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models import Note,User
import os
import uuid
import shutil

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

#Upload a note
def create_note_service(title:str,description:str,subject:str,is_private:bool,file:UploadFile,db:Session,current_user:User):
    if not file.filename.endswith((".pdf",".doc",".docx")):
        raise HTTPException(status_code=400,
                            detail="Invalid file type")
    unique_name=f"{uuid.uuid4()}_{file.filename}"
    file_path=os.path.join(UPLOAD_DIR,unique_name)

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

        new_note=Note(
            owner_id=current_user.id,
            title=title,
            description=description,
            subject=subject,
            is_private=is_private,
            file_path=file_path,
        )
        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        return new_note
    
#View all notes created by yourself    
def view_my_notes_service(db:Session,current_user:User):
    notes=db.query(Note).filter(Note.owner_id==current_user.id).all()
    return notes

#View a specific note
def get_note_file_service(note_id:int,db:Session,current_user:User):
    note=db.query(Note).filter(Note.id==note_id,Note.owner_id==current_user.id).first()
    if not note:
        raise HTTPException(status_code=404,
                            detail="Note not found")
    if not os.path.exists(note.file_path):
        raise HTTPException(status_code=404,
                            detail="File missing")
    return FileResponse(
        path=note.file_path,
        filename=os.path.basename(note.file_path),
        media_type="application/octet-stream"
    )