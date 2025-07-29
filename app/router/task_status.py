# app/router/task_status.py
from fastapi import APIRouter
from celery.result import AsyncResult
from app.worker.celery import celery_app

router = APIRouter()

# Task 상태 조회 엔드포인트
@router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
