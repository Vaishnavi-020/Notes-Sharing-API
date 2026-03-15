from fastapi import APIRouter,Depends,UploadFile,File,Form,Request
from sqlalchemy.orm import Session
from app.services.notes_services import create_note_service,get_my_notes_service,get_public_notes_service,get_note_file_service,download_note_file_service,edit_note_service,delete_note_service,search_notes_service
from app.schemas.notes_schema import NoteOut,NoteUpdate
from app.schemas.paginated_schema import PaginatedResponse
from app.models.users import User
from app.database import get_db
from app.dependencies import get_current_user,get_current_user_optional,pagination_params
import math

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


@router.get('/my_notes',response_model=PaginatedResponse[NoteOut])
def get_my_notes(db:Session=Depends(get_db),current_user=Depends(get_current_user),pagination:dict=Depends(pagination_params)):
    return get_my_notes_service(db,current_user,pagination)


@router.get("/search",response_model=PaginatedResponse[NoteOut])
def search_notes(q:str,
                 db:Session=Depends(get_db),
                 current_user:User|None=Depends(get_current_user_optional),
                 pagination:dict=Depends(pagination_params)):
    total,notes=search_notes_service(db=db,query=q,current_user=current_user,offset=pagination["offset"],limit=pagination["limit"],)
    total_pages=math.ceil(total/pagination["limit"])
    return{
        "total":total,
        "page":pagination["page"],
        "limit":pagination["limit"],
        "total_pages":total_pages,
        "items":notes,
    }

@router.get("/public_notes",response_model=PaginatedResponse[NoteOut])
def get_public_notes(db:Session=Depends(get_db),current_user:User|None=Depends(get_current_user_optional),pagination:dict=Depends(pagination_params)):
    total,notes=get_public_notes_service(db,current_user,pagination)
    total_pages=math.ceil(total/pagination["limit"])
    return {
        "total":total,
        "page":pagination["page"],
        "limit":pagination["limit"],
        "total_pages":total_pages,
        "items":notes
    }

@router.get('/{note_id}',response_model=NoteOut)
def get_note_file(note_id:int,db:Session=Depends(get_db),current_user:User|None=Depends(get_current_user_optional)):
    return get_note_file_service(note_id,db,current_user)

@router.get("/{note_id}/download")
def download_note_file(note_id:int,request:Request,db:Session=Depends(get_db),current_user:User|None=Depends(get_current_user_optional)):
    return download_note_file_service(note_id,request,db,current_user)

@router.put("/{note_id}")
def edit_note(note_id:int,note_data:NoteUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return edit_note_service(note_id,note_data,db,current_user)

@router.delete("/{note_id}")
def delete_note(note_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return delete_note_service(note_id,db,current_user)


