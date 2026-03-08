import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from fastapi import HTTPException
from app.schemas.ai_schema import AIRequest
from sqlalchemy.orm import Session
from app.models import Note,User

genai.configure(api_key=GEMINI_API_KEY)

model=genai.GenerativeModel("gemini-2.5-flash")

def ask_ai_about_note_service(note_id:int,note_data:AIRequest,db:Session,current_user:User|None):

    note=db.query(Note).filter(Note.id==note_id).first()
    if not note:
        return{"Error":"Note not found"}
    if note.is_private:
        if not current_user or note.owner_id!=current_user.id:
            raise HTTPException(403,
                                detail="You cannot access this note.")
    note_text=note.content
    question=note_data.question

    prompt=f"""
        You are a helpful assistant.
        The user has the following notes:
        {note_text}

        Question:
        {question}

        Answer the question based only on the notes.
        """
    response=model.generate_content(prompt)
    return response.text
