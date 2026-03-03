from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteOut(BaseModel):
    id:int
    title:str
    description:str
    subject:str
    is_private:bool
    created_at:datetime

    class Config:
        from_attributes=True

class NoteUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None

