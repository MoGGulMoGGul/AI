import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_url(url: str):
    """
    URL을 분석하여, 네이버 블로그인 경우 Playwright를 사용하고
    그 외에는 일반적인 방식으로 텍스트를 추출합니다.
    """
    # URL에 'blog.naver.com'이 포함되어 있는지 확인
    if "blog.naver.com" in url:
        logger.info(f"네이버 블로그 URL 감지: {url}. Playwright를 사용하여 처리합니다.")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, timeout=20000, wait_until='domcontentloaded')

                # 여러 후보 선택자를 시도하여 가장 적합한 본문 영역을 찾음
                content_selectors = [
                    "div.se-main-container",  # 최신 스마트에디터 원
                    "div.post_content",        # 구버전 스마트에디터
                    "div.blog_content",        # 또 다른 구버전
                    "div.article",             # 일반적인 블로그 아티클
                    "body"                     # 최종 폴백: body 전체
                ]
                
                content_html = page.content()
                soup = BeautifulSoup(content_html, 'html.parser')
                text = ""

                for selector in content_selectors:
                    if selector == "body":
                        # body 태그는 마지막 시도
                        text = soup.body.get_text(separator='\n', strip=True)
                        break

                    main_content = soup.select_one(selector)
                    if main_content:
                        text = main_content.get_text(separator='\n', strip=True)
                        if len(text.strip()) > 50:  # 최소한의 텍스트가 추출되었는지 확인
                            logger.info(f"선택자 '{selector}'를 사용하여 텍스트를 성공적으로 추출했습니다.")
                            break
                        else:
                            text = "" # 텍스트가 너무 적으면 다음 선택자를 시도

                if not text:
                    raise ValueError("페이지에서 유효한 본문 텍스트를 추출할 수 없습니다.")
                
                browser.close()
                return "네이버 블로그", text

        except Exception as e:
            logger.error(f"Playwright로 네이버 블로그 처리 중 오류 발생: {e}")
            # 오류 발생 시 일반 방식으로 재시도합니다.
            return extract_text_with_requests(url)
    else:
        # 네이버 블로그가 아니면 기존의 빠른 방식을 사용합니다.
        return extract_text_with_requests(url)

def extract_text_with_requests(url: str):
    """requests와 BeautifulSoup을 사용하여 웹페이지 텍스트를 추출하는 일반적인 방법입니다."""
    logger.info(f"일반 방식으로 URL 처리: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.body.get_text(separator='\n', strip=True)
        return content_type, text
    except requests.RequestException as e:
        logger.error(f"requests로 URL 처리 중 오류 발생: {e}")
        return "에러", f"URL 콘텐츠를 가져오는 데 실패했습니다: {e}"