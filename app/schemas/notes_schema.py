from pydantic import BaseModel

class NotesOut(BaseModel):
    id:int
    title:str

    class Config:
        from_attributes=True

