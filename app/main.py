from fastapi import FastAPI
from app.routes.example import router as ex_router
from app.database import engine
from app.models.base import Base
from app.routes.auth import router as auth_router
from app.routes.note import router as note_router

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ex_router)
app.include_router(auth_router)
app.include_router(note_router)