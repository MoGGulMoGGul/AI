import os
import requests
from app.celery_config import celery_app
from app.extractor import extract_text_from_url
from app.text_filter import clean_text
from app.langchain_pipe import run_langchain_pipeline
from app.thumbnail_handler import generate_thumbnail_and_upload_to_s3
from app.video_handler import get_combined_transcript
from app.image_handler import process_image_tip
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task
def process_url_task(url):
    """
    URL의 콘텐츠 타입(웹, 유튜브, 이미지)을 감지하고,
    각각에 맞는 요약, 태그, 썸네일 생성을 실행한 후 결과만 반환하는 Celery 작업입니다.
    (폴링 방식이므로 콜백 로직은 없습니다.)
    """
    try:
        # 1. 썸네일 생성 및 S3 업로드 (가장 먼저 시도)
        s3_thumbnail_url = generate_thumbnail_and_upload_to_s3(url)
        if not s3_thumbnail_url:
            logger.warning(f"URL '{url}'에 대한 썸네일 생성/업로드에 실패했습니다.")

        # 2. 콘텐츠 타입 감지 및 처리
        headers = requests.head(url, timeout=10, allow_redirects=True).headers
        content_type = headers.get("Content-Type", "").lower()
        
        result_data = {}

        # 이미지 처리
        if "image" in content_type:
            logger.info(f"콘텐츠 타입 '이미지' 감지: {url}")
            image_result = process_image_tip(url)
            result_data = {
                "type": "이미지",
                "title": image_result['summary_and_tags'].get('title', '이미지 분석 결과'),
                "summary": image_result['summary_and_tags'].get('summary'),
                "tags": image_result['summary_and_tags'].get('tags', [])
            }
        # 유튜브 처리
        elif "youtube.com" in url or "youtu.be" in url:
            logger.info(f"콘텐츠 타입 '유튜브' 감지: {url}")
            full_text = get_combined_transcript(url)
            cleaned_text = clean_text(full_text)
            yt_result = run_langchain_pipeline(cleaned_text)
            result_data = {
                "type": "유튜브",
                "title": yt_result.get('title'),
                "summary": yt_result.get('summary'),
                "tags": yt_result.get('tags', [])
            }
        # 웹페이지 처리 (기본값)
        else:
            logger.info(f"콘텐츠 타입 '웹페이지' 감지: {url}")
            # extract_text_from_url은 (content_type, text_content) 튜플을 반환
            extracted_content_type, text_content = extract_text_from_url(url)
            if not text_content:
                raise ValueError("웹페이지에서 텍스트를 추출할 수 없습니다.")
            
            cleaned_text = clean_text(text_content)
            web_result = run_langchain_pipeline(cleaned_text)
            result_data = {
                "type": extracted_content_type, # extractor가 반환한 타입 사용
                "title": web_result.get('title'),
                "summary": web_result.get('summary'),
                "tags": web_result.get('tags', [])
            }

        # 3. 최종 결과에 썸네일 URL 추가
        result_data["thumbnail_url"] = s3_thumbnail_url
        
        logger.info(f"URL '{url}' 처리가 성공적으로 완료되었습니다.")
        return result_data

    except Exception as e:
        logger.error(f"URL '{url}' 처리 중 오류 발생: {e}", exc_info=True)
        # Celery가 작업을 실패로 기록하도록 예외를 다시 발생시킴
        raise