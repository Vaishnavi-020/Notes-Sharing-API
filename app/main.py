from fastapi import FastAPI
from app.routes.example import router as ex_router

app=FastAPI()

app.include_router(ex_router)