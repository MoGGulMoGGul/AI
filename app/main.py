# app/main.py
from fastapi import FastAPI
from app.router import async_pipeline, task_status
from app.router import search

app = FastAPI()
app.include_router(async_pipeline.router)
app.include_router(task_status.router)
app.include_router(search.router)