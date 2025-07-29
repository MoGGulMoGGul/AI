# app/router/async_pipeline.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.worker.tasks import process_url_task

router = APIRouter()

class URLRequest(BaseModel):
    url: str

@router.post("/async-process/")
def async_process_url(request: URLRequest):
    try:
        task = process_url_task.delay(request.url)
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
