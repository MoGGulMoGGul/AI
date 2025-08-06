# app/summarizer.py

from app.celery_config import celery_app
from app.extractor import extract_text_from_url
from app.video_handler import get_combined_transcript
from app.text_filter import clean_text
from app.ai_utils import summarize_and_tag
from app.langchain_pipe import run_langchain_pipeline
import requests

@celery_app.task(name="app.summarizer.process_url_task")
def process_url_task(url: str):
    try:
        headers = requests.head(url, timeout=5).headers
        content_type = headers.get("Content-Type", "")

        if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]) or "image" in content_type:
            # 이미지 처리
            local_filename = "temp_image.jpg"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            result = process_image_tip(local_filename)
            return f"[이미지] 제목: {result['title']} / 요약: {result['summary']} / 태그: {', '.join(result['tags'])}"

        elif "youtube.com" in url or "youtu.be" in url:
            # 유튜브 처리
            full_text = get_combined_transcript(url)
            cleaned_text = clean_text(full_text)
            result = summarize_and_tag(cleaned_text)
            return f"[유튜브] 제목: {result['title']} / 요약: {result['summary']} / 태그: {', '.join(result['tags'])}"

        else:
            # 일반 텍스트 웹페이지 처리
            text = extract_text_from_url(url)
            result = run_langchain_pipeline(text)
            return f"[웹페이지] 제목: {result['title']} / 요약: {result['summary']} / 태그: {', '.join(result['tags'])}"

    except Exception as e:
        return f"[에러] 처리 실패: {e}"
