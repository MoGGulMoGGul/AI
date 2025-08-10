# app/thumbnail_handler.py

import requests
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright 
from app.video_handler import extract_video_id

THUMBNAIL_SIZE = (256, 256)

def _create_thumbnail_from_image_url(url: str) -> bytes:
    """이미지 URL에서 직접 썸네일을 생성합니다."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.thumbnail(THUMBNAIL_SIZE)
        
        byte_arr = BytesIO()
        img.save(byte_arr, format='PNG')
        return byte_arr.getvalue()
    except Exception as e:
        print(f"[Error] 이미지 썸네일 생성 실패: {e}")
        return None

def _get_youtube_thumbnail_url(url: str) -> str:
    """YouTube URL에서 고화질 썸네일 주소를 반환합니다."""
    video_id = extract_video_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    return None

def _create_thumbnail_from_webpage(url: str) -> bytes: 
    """Playwright를 사용하여 웹페이지 스크린샷으로 썸네일을 생성합니다."""
    try:
        with sync_playwright() as p: 
            browser = p.chromium.launch(headless=True) 
            page = browser.new_page() 
            page.goto(url, timeout=15000) 
            page.wait_for_timeout(2000) 
            
            screenshot_bytes = page.screenshot() 
            browser.close()

            img = Image.open(BytesIO(screenshot_bytes))
            img.thumbnail(THUMBNAIL_SIZE)

            byte_arr = BytesIO()
            img.save(byte_arr, format='PNG')
            return byte_arr.getvalue()
    except Exception as e:
        print(f"[Error] 웹페이지 썸네일 생성 실패: {e}")
        return None

def generate_thumbnail(url: str) -> tuple[bytes | str | None, str]:
    """URL 유형에 따라 적절한 썸네일 생성 함수를 호출합니다."""
    # 1. YouTube URL인 경우
    if "youtube.com" in url or "youtu.be" in url:
        yt_thumb_url = _get_youtube_thumbnail_url(url)
        if yt_thumb_url:
            try:
                response = requests.get(yt_thumb_url, timeout=10)
                response.raise_for_status()
                return response.content, "image"
            except requests.RequestException as e:
                print(f"[Error] 유튜브 썸네일 다운로드 실패: {e}")
                return None, "error"

    # 2. 헤더를 통해 이미지 URL인지 확인
    try:
        headers = requests.head(url, timeout=5, allow_redirects=True).headers
        content_type = headers.get('Content-Type', '')
        if 'image' in content_type:
            thumb_data = _create_thumbnail_from_image_url(url)
            return thumb_data, "image"
    except requests.RequestException:
        pass

    # 3. 일반 웹페이지로 간주하고 스크린샷 생성
    thumb_data = _create_thumbnail_from_webpage(url) 
    return thumb_data, "image"
