# app/image_handler.py
import easyocr
from app.text_filter import clean_text
from app.ai_utils import summarize_and_tag

reader = easyocr.Reader(['ko', 'en'])  # 한글 + 영어 지원

def extract_text_from_image(image_path: str) -> str:
    results = reader.readtext(image_path, detail=0)
    raw_text = "\n".join(results)
    return raw_text

def process_image_tip(image_path: str) -> dict:
    raw_text = extract_text_from_image(image_path)
    cleaned_text = clean_text(raw_text)
    summary_and_tags = summarize_and_tag(cleaned_text)  # 실제 요약 실행

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "summary_and_tags": summary_and_tags  # 결과 반영
    }
