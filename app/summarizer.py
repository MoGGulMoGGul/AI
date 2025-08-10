# app/summarizer.py

from app.celery_config import celery_app
from app.extractor import extract_text_from_url
from app.video_handler import get_combined_transcript
from app.text_filter import clean_text
from app.ai_utils import summarize_and_tag
from app.langchain_pipe import run_langchain_pipeline
import requests
from app.image_handler import process_image_tip
from app.thumbnail_handler import generate_thumbnail
import base64 # Base64 인코딩/디코딩을 위해 임포트

@celery_app.task(name="app.summarizer.process_url_task")
def process_url_task(url: str): 
    try:
        headers = requests.head(url, timeout=5).headers
        content_type = headers.get("Content-Type", "")

        thumbnail_data = None
        thumbnail_type = None
        try:
            thumbnail_raw_data, thumb_type = generate_thumbnail(url) 

            if thumbnail_raw_data:
                if thumb_type == "image":
                    thumbnail_data = base64.b64encode(thumbnail_raw_data).decode('utf-8')
                elif thumb_type == "redirect":
                    thumbnail_data = thumbnail_raw_data
                else:
                    thumbnail_data = None
            else:
                thumbnail_data = None
        except Exception as e:
            print(f"[Error] 썸네일 생성 중 오류 발생: {e}")
            thumbnail_data = None
            thumbnail_type = None


        if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]) or "image" in content_type:
            local_filename = "temp_image.jpg"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            result = process_image_tip(local_filename)
            return {
                "type": "이미지",
                "title": result['summary_and_tags']['title'],
                "summary": result['summary_and_tags']['summary'],
                "tags": result['summary_and_tags']['tags'],
                "thumbnail_data": thumbnail_data,
                "thumbnail_type": thumb_type
            }


        elif "youtube.com" in url or "youtu.be" in url:
            full_text = get_combined_transcript(url)
            cleaned_text = clean_text(full_text)
            result = summarize_and_tag(cleaned_text)
            return {
                "type": "유튜브",
                "title": result['title'],
                "summary": result['summary'],
                "tags": result['tags'],
                "thumbnail_data": thumbnail_data,
                "thumbnail_type": thumb_type
            }

        else:
            text = extract_text_from_url(url)
            result = run_langchain_pipeline(text)
            return {
                "type": "웹페이지",
                "title": result['title'],
                "summary": result['summary'],
                "tags": result['tags'],
                "thumbnail_data": thumbnail_data,
                "thumbnail_type": thumb_type
            }

    except Exception as e:
        return {
            "type": "에러",
            "title": "요약 실패",
            "summary": f"처리 실패: {e}",
            "tags": ["오류"],
            "thumbnail_data": None,
            "thumbnail_type": None
        }
