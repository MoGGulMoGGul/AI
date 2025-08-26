# app/celery_config.py
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

# Redis 연결 설정을 환경변수에서 가져오되, 기본값 설정
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "app",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['app.summarizer']
)

# Celery 설정 최적화
celery_app.conf.update(
    # 작업 설정
    task_annotations={
        'app.summarizer.process_url_task': {'rate_limit': '10/m'}
    },
    # 직렬화 설정
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    
    # 시간대 설정
    timezone='Asia/Seoul',
    enable_utc=True,
    
    # Redis 연결 최적화
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    
    # 결과 만료 시간 (1시간)
    result_expires=3600,
    
    # Worker 최적화
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    
    # 메모리 누수 방지
    worker_max_tasks_per_child=50,
)