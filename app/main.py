from fastapi import FastAPI
from app.routes.example import router as ex_router
from app.database import engine
from app.models.base import Base
from app.routes.auth import router as auth_router
from app.routes.note import router as note_router
from app.routes.ai import router as ai_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(ex_router)
app.include_router(auth_router)
app.include_router(note_router)
app.include_router(ai_router)