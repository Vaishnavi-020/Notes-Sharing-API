from pydantic import BaseModel

class AIRequest(BaseModel):
    note_id:int
    question:str