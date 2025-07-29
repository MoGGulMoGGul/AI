# app/worker/celery.py
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Redis 브로커 주소
    backend="redis://localhost:6379/0"  # 결과 저장소도 Redis로 설정
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Seoul",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["app.worker"])
