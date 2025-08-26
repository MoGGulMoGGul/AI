# app/image_handler.py
import easyocr
from app.text_filter import clean_text
from app.ai_utils import summarize_and_tag

# reader 객체를 전역 변수로 선언하되, 초기화는 하지 않습니다.
reader = None

def get_ocr_reader():
    """
    easyocr.Reader 객체를 한 번만 생성하여 재사용하는 함수 (지연 초기화).
    """
    global reader
    if reader is None:
        print("Initializing EasyOCR reader for the first time...")
        # 필요한 모델을 처음 사용할 때만 다운로드하고 초기화합니다.
        reader = easyocr.Reader(['ko', 'en'])
        print("EasyOCR reader initialized.")
    return reader

def extract_text_from_image(image_path: str) -> str:
    # get_ocr_reader() 함수를 통해 reader 객체를 가져옵니다.
    ocr_reader = get_ocr_reader()
    results = ocr_reader.readtext(image_path, detail=0)
    raw_text = "\n".join(results)
    return raw_text

def process_image_tip(image_path: str) -> dict:
    raw_text = extract_text_from_image(image_path)
    cleaned_text = clean_text(raw_text)
    summary_and_tags = summarize_and_tag(cleaned_text)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "summary_and_tags": summary_and_tags
    }
