from pydantic import BaseModel
from typing import Optional

class NoteOut(BaseModel):
    id:int
    title:str
    description:str
    subject:str
    is_private:bool

    class Config:
        from_attributes=True

class NoteUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None

