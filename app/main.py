from fastapi import FastAPI
from app.routes.example import router as ex_router
from app.database import engine
from app.models.base import Base
import app.models

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ex_router)