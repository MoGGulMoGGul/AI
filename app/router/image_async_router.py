# app/routers/image_async_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.image_worker.tasks import process_image_url_task

router = APIRouter()

class ImageAsyncRequest(BaseModel):
    url: str

@router.post("/async-image-process/")
def async_image_process(req: ImageAsyncRequest):
    task = process_image_url_task.delay(req.url)
    return {"task_id": task.id}
