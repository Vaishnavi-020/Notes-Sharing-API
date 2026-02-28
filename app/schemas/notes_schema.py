from pydantic import BaseModel
from typing import Optional

class NotesOut(BaseModel):
    id:int
    title:str

    class Config:
        from_attributes=True

class NoteUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None

