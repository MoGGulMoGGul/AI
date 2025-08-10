# app/celery_config.py

from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery_app = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.autodiscover_tasks(["app"])

celery_app.conf.update(
    task_annotations = {'app.summarizer.process_url_task': {'rate_limit': '10/m'}},
)

import app.summarizer
