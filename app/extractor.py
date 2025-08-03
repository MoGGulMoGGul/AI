# app/extractor.py
from app.playwright_handler import extract_html_with_playwright
from app.structure_detector import extract_main_content_from_html
from app.text_filter import clean_text
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str) -> str:
    try:
        # Step 1: 시도 1차 - requests로 HTML 받아오기
        response = requests.get(url, timeout=10)
        html = response.text

        # Step 2: 정적 HTML에서 본문 찾기
        content = extract_main_content_from_html(html)
        if content and len(content) > 100:
            return clean_text(content)

        # Step 3: 실패 시 playwright로 JS 렌더링된 HTML 받아오기
        html = extract_html_with_playwright(url)
        content = extract_main_content_from_html(html)
        return clean_text(content) if content else "본문 추출 실패"

    except Exception as e:
        return f"[에러] 본문 추출 중 오류 발생: {e}"
