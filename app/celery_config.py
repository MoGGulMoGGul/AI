# app/celery_config.py
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    # 작업이 포함된 모듈을 명시적으로 포함하여 안정성을 높입니다.
    include=['app.summarizer']
)

# 'include' 옵션을 사용하므로 autodiscover_tasks는 더 이상 필요하지 않습니다.
# celery_app.autodiscover_tasks(["app"])

celery_app.conf.update(
    task_annotations={'app.summarizer.process_url_task': {'rate_limit': '10/m'}},
)
