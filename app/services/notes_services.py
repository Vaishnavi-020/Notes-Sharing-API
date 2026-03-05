from fastapi import HTTPException,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Note,User
from app.schemas.notes_schema import NoteUpdate
import os
import uuid
import shutil
import math

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

#Upload a note
def create_note_service(title:str,description:str,subject:str,is_private:bool,file:UploadFile,db:Session,current_user:User):
    if not file.filename.endswith((".pdf",".doc",".docx")):
        raise HTTPException(status_code=400,
                            detail="File should be in pdf,doc or docx format only")
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

#View all private notes
def get_my_notes_service(db:Session,current_user:User,pagination:dict):
    total=db.query(Note).filter(Note.owner_id==current_user.id).count()
    notes=db.query(Note).filter(Note.owner_id==current_user.id).offset(pagination["offset"]).limit(pagination["limit"]).all()
    total_pages=math.ceil(total/pagination["limit"])
    return {
        "total":total,
        "page":pagination["page"],
        "limit":pagination["limit"],
        "total_pages":total_pages,
        "items":notes,
    }


#View public notes
def get_public_notes_service(db:Session,current_user:User|None,pagination:dict):
    base_query=db.query(Note).filter(Note.is_private==False)
    total=base_query.count()
    notes=(base_query.offset(pagination["offset"])
           .limit(pagination["limit"])
           .all())
    return total,notes

#View a specific note
def get_note_file_service(note_id:int,db:Session,current_user:User | None):
    note=db.query(Note).filter(Note.id==note_id).first()
    if not note:
        raise HTTPException(status_code=404,
                            detail="Note not found")
    if note.is_private:
        if not current_user or note.owner_id!=current_user.id:
            raise HTTPException(status_code=403,
                                detail="Not authorized")
    if not os.path.exists(note.file_path):
        raise HTTPException(status_code=404,
                            detail="File missing")
    return FileResponse(
        path=note.file_path,
        filename=os.path.basename(note.file_path),
        media_type="application/octet-stream"
    )

#Edit note
def edit_note_service(note_id:int,note_data:NoteUpdate,db:Session,current_user:User):
    note=db.query(Note).filter(Note.id==note_id,Note.owner_id==current_user.id).first()
    if not note:
        raise HTTPException(status_code=404,
                            detail="Note not found")
    if note_data.title is not None:
        note.title=note_data.title
    if note_data.description is not None:
        note.description=note_data.description
    
    db.commit()
    db.refresh(note)

    return note

#Delete note
def delete_note_service(note_id:int,db:Session,current_user:User):
    note=db.query(Note).filter(Note.id==note_id,Note.owner_id==current_user.id).first()
    if not note:
        raise HTTPException(status_code=400,
                            detail="Note not found")
    db.delete(note)
    db.commit()

    return {
        "message":"Note deleted successfully"
    }

#Search note
def search_notes_service(db:Session,query:str,current_user:User|None,offset:int,limit:int):
    search_filter=(or_(Note.title.ilike(f"%{query}%"),
                                    Note.description.ilike(f"%{query}%"),
                                    Note.subject.ilike(f"%{query}%"),
                                    ))
    
    base_query=db.query(Note).filter(search_filter)

    if current_user is None:
        base_query=base_query.filter(Note.is_private==False)

    else:
        base_query=base_query.filter(
            or_(
                Note.is_private==False,
                Note.owner_id==current_user.id,
            )
        )
    total=base_query.count()
    notes=(base_query.offset(offset).limit(limit).all())
    return total,notes