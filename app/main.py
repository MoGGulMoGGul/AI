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
from app.summarizer import process_url_task
from celery.result import AsyncResult
from app.celery_config import celery_app
from app.ai_utils import summarize_and_tag
from app.thumbnail_handler import generate_thumbnail

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.post("/async-index/")
def async_index(request: URLRequest):
    task = process_url_task.delay(request.url)
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"status": result.status, "result": result.result if result.ready() else None}


# 요약 결과 조회 엔드포인트 (Spring Boot에서 호출)
@app.get("/summary-result/{task_id}")
def get_summary_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    
    if not result.ready():
        raise HTTPException(status_code=202, detail="요약 작업이 아직 완료되지 않았습니다. 잠시 후 다시 시도해주세요.")
    
    if result.successful():
        task_output = result.result # 딕셔너리 형태
        if isinstance(task_output, dict):
            # thumbnail_data 대신 thumbnail_url을 반환하도록 수정
            return {
                "summary": task_output.get("summary", "요약 없음"),
                "title": task_output.get("title", "제목 없음"),
                "tags": task_output.get("tags", []),
                "thumbnail_url": task_output.get("thumbnail_url")
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