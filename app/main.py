# app/main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.extractor import extract_text_from_url
from app.image_handler import process_image_tip
from app.video_handler import get_combined_transcript
from app.text_filter import clean_text
from app.langchain_pipe import run_langchain_pipeline
from app.qa_api import router as qa_router
from app.tasks import process_url_task
from celery.result import AsyncResult
from app.celery_worker import celery_app
from app.summarizer import summarize_and_tag  # API 키 연결 시 사용
from app.elasticsearch_client import search_by_tag  # 🔍 태그 검색 함수 불러오기

app = FastAPI()
app.include_router(qa_router)

# ✅ URL 기반 텍스트 추출 (정적/동적 웹페이지)
class URLRequest(BaseModel):
    url: str

@app.post("/extract")
def extract(request: URLRequest):
    text = extract_text_from_url(request.url)
    return {"text": text}

# ✅ 이미지 기반 꿀팁 추출 (EasyOCR)
@app.post("/extract-image-tip")
async def extract_image_tip(file: UploadFile = File(...)):
    with open(f"temp_{file.filename}", "wb") as f:
        content = await file.read()
        f.write(content)

    result = process_image_tip(f"temp_{file.filename}")
    return result

# ✅ 유튜브 영상 기반 꿀팁 추출 (자막 + Whisper + GPT 요약)
class VideoRequest(BaseModel):
    url: str

@app.post("/extract-video-tip")
def extract_video_tip(request: VideoRequest):
    full_text = get_combined_transcript(request.url)
    cleaned_text = clean_text(full_text)
    summary_and_tags = summarize_and_tag(cleaned_text)

    return {
        "raw_text": full_text,
        "cleaned_text": cleaned_text,
        "summary_and_tags": summary_and_tags
    }

# ✅ 텍스트 인덱싱
class IndexRequest(BaseModel):
    text: str

@app.post("/index-tip")
def index_tip(request: IndexRequest):
    count = run_langchain_pipeline(request.text)
    return {"message": f"{count} chunks indexed"}

# ✅ 비동기 URL 처리
@app.post("/async-index/")
def async_index(request: URLRequest):
    task = process_url_task.delay(request.url)
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "status": result.status,
        "result": result.result if result.ready() else None,
    }

@app.get("/search-tag")
def search_tag(tag: str):
    """
    🔍 태그로 팁 검색 (Elasticsearch 사용)
    예: /search-tag?tag=시간
    """
    results = search_by_tag(tag)
    return [hit["_source"] for hit in results["hits"]["hits"]]



# taskkill /F /IM python.exe
# uvicorn app.main:app

# 도커 컴포즈 실행(레디스,셀러리)
# docker-compose up --build

# Celery 워커
# celery -A app.celery_worker.celery_app worker --loglevel=info

# docker exec -it momo_postgres psql -U user -d momo
# -- ① pgvector 확장 설치 확인
# \dx

# -- ② tip_data 테이블 생성 여부 확인
# \dt

# -- ③ 데이터 유무 확인 (없어도 됨)
# SELECT * FROM tip_data;

# ✅ 1. 현재 .venv 삭제 명령어 (Windows PowerShell 기준)
# Remove-Item -Recurse -Force .venv

#✅ 2. 나중에 다시 .venv를 만드는 명령어 (재설치용)

# 1. 가상환경 생성
#python -m venv .venv

# 2. 가상환경 활성화
#.\.venv\Scripts\activate

# 3. 패키지 설치
#pip install -r requirements.txt