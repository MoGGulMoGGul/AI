# app/main.py
import asyncio
import sys

print("="*50)
print(f"스크립트 시작. 현재 플랫폼: {sys.platform}")
print(f"초기 asyncio 정책: {asyncio.get_event_loop_policy().__class__.__name__}")
if sys.platform == "win32":
    print("Windows 플랫폼 감지. 정책 변경을 시도합니다...")
    try:
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
        print(f"정책 변경 완료. 새로운 asyncio 정책: {asyncio.get_event_loop_policy().__class__.__name__}")
    except Exception as e:
        print(f"정책 변경 중 오류 발생: {e}")
else:
    print("Windows 플랫폼이 아니므로 정책을 변경하지 않습니다.")
print("="*50)

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response, RedirectResponse

from app.extractor import extract_text_from_url
from app.image_handler import process_image_tip
from app.video_handler import get_combined_transcript
from app.text_filter import clean_text
from app.langchain_pipe import run_langchain_pipeline
from app.qa_api import router as qa_router

from app.summarizer import process_url_task
from celery.result import AsyncResult
# ✅ 같은 인스턴스 사용
from app.celery_config import celery_app

# ✅ 잘못된 import 수정
from app.ai_utils import summarize_and_tag
from app.elasticsearch_client import search_by_tag
from app.thumbnail_handler import generate_thumbnail

app = FastAPI()
app.include_router(qa_router)

class URLRequest(BaseModel):
    url: str

@app.post("/extract")
def extract(request: URLRequest):
    text = extract_text_from_url(request.url)
    return {"text": text}

@app.post("/extract-image-tip")
async def extract_image_tip(file: UploadFile = File(...)):
    with open(f"temp_{file.filename}", "wb") as f:
        content = await file.read()
        f.write(content)
    return process_image_tip(f"temp_{file.filename}")

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

class IndexRequest(BaseModel):
    text: str

@app.post("/index-tip")
def index_tip(request: IndexRequest):
    out = run_langchain_pipeline(request.text)
    return {
        "message": f"{out['chunks']} chunks indexed",
        "title": out["title"],
        "tags": out["tags"]
    }

@app.post("/async-index/")
def async_index(request: URLRequest):
    task = process_url_task.delay(request.url)
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"status": result.status, "result": result.result if result.ready() else None}

@app.get("/search-tag")
def search_tag(tag: str):
    """Elasticsearch 태그 검색"""
    hits = search_by_tag(tag)
    return [hit["_source"] for hit in hits]

# 요약 결과 조회 엔드포인트 (Spring Boot에서 호출)
@app.get("/summary-result/{task_id}")
def get_summary_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    
    if not result.ready():
        raise HTTPException(status_code=202, detail="요약 작업이 아직 완료되지 않았습니다. 잠시 후 다시 시도해주세요.")
    
    if result.successful():
        task_output = result.result # 딕셔너리 형태
        if isinstance(task_output, dict):
            return {
                "summary": task_output.get("summary", "요약 없음"),
                "title": task_output.get("title", "제목 없음"),
                "tags": task_output.get("tags", []),
                "thumbnail_data": task_output.get("thumbnail_data"), 
                "thumbnail_type": task_output.get("thumbnail_type") 
            }
        else:
            raise HTTPException(status_code=500, detail=f"요약 결과 형식이 올바르지 않습니다: {task_output}")
    else:
        raise HTTPException(status_code=500, detail=f"요약 작업이 실패했습니다: {result.result}")


# 썸네일 생성
@app.post("/thumbnail")
async def create_thumbnail(request: URLRequest):
    """
    URL을 받아 콘텐츠 유형에 맞는 썸네일을 생성합니다.
    - 유튜브: 썸네일 URL로 리다이렉트
    - 이미지/웹페이지: PNG 바이트 반환
    """
    thumbnail_data, thumb_type = generate_thumbnail(request.url)

    if not thumbnail_data:
        return Response(content="썸네일 생성에 실패했습니다.", status_code=500)

    if thumb_type == "redirect":
        return RedirectResponse(url=thumbnail_data)

    return Response(content=thumbnail_data, media_type="image/png")


# taskkill /F /IM python.exe
# uvicorn app.main:app

# 첫 실행(또는 이미지 새로 빌드가 필요할 때)
# docker compose up -d --build

#실행(빌드 없이 전부 백그라운드로)

# docker compose up -d --no-build

#잠깐 멈췄다가 다시 켜고 싶을 때

# docker compose stop     # 컨테이너 '중지' (네트워크/볼륨/이미지 유지)
# docker compose start    # 다시 시작

# 컨테이너를 아예 내려서 깨끗이 재생성하고 싶을 때

# docker compose down     # 컨테이너 + 네트워크 제거(볼륨은 그대로)

# 완전 초기화(데이터까지 삭제, 주의!):

# docker compose down -v

# git status
# git add -A
# git commit -m "메시지"
# git push origin <브랜치명>   # 예: main