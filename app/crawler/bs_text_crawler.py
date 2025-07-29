# BeautifulSoup 기반 일반 클롤러
# 정적 웹페이지용 requests + BeautifulSoup 조합

"""
# bs_crawler.py의 흐름
    1. url 입력
    2. requests로 HTML 콘텐츠 가져오기
    3. BeautifulSoup으로 HTML 파싱
    4. 불필요한 공백/개행 제거
    5. 결과 텍스트 반환
"""

import requests
from bs4 import BeautifulSoup
from .base import BaseCrawler
from .utils import clean_html
from urllib.parse import urljoin


class BeautifulSoupCrawler(BaseCrawler):
    # 크롤링 메서드 실제 구현
    # self : 그 클래스의 인스턴스 자신을 가리키는 변수(BeautifulSoupCrawler 클래스가 생성된 후, 그 객체 자신을 뜻함)
    def crawl(self, url) -> str:
        try:
            # requests로 HTML 콘텐츠 가져오기 -> http 요청 보내기
            headers = {
                "User-Agent": ( # User-Agent는 웹 브라우저의 정보를 담고 있는 헤더로, 서버가 요청을 처리하는데 참고함
                                # 크롤러가 아닌 일반 브라우저로 요청하는 것처럼 보이게 하기 위해 설정
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=10)
            # 요청이 성공하지 않으면 예외 발생(응답 코드가 200이 아닐 때)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"[BeautifulSoup] 크롤링 실패: {e}")

        soup = BeautifulSoup(response.content, "html.parser")

        # 네이버 블로그일 경우 iframe 본문 링크로 다시 요청
        if "blog.naver.com" in url:
            iframe = soup.find("iframe", id="mainFrame")
            if iframe and iframe.get("src"):
                iframe_url = urljoin(url, iframe["src"])
                try:
                    iframe_response = requests.get(iframe_url, headers=headers, timeout=10)
                    iframe_response.raise_for_status()
                except requests.RequestException as e:
                    raise RuntimeError(f"[BeautifulSoup] iframe 요청 실패: {e}")
                soup = BeautifulSoup(iframe_response.content, "html.parser")

        # 본문 추출 (일반 블로그 or 네이버 본문)
        candidates = [
            soup.find("div", class_="se-main-container"),   # 신형 에디터
            soup.find("div", class_="post-view"),           # 구형 에디터
            soup.find("div", id="postViewArea"),            # 일부 구형
        ]

        for candidate in candidates:
            if candidate:
                text = candidate.get_text(separator="\n")
                print("[DEBUG] 본문 일부:\n", text[:500])
                return clean_html(text)

        # fallback: 모든 텍스트 가져오기
        text = soup.get_text(separator="\n")
        print("[DEBUG] 전체 본문 fallback 사용:\n", text[:500])
        return clean_html(text)
    

def crawl_text_from_url(url: str) -> str:
    crawler = BeautifulSoupCrawler()
    return crawler.crawl(url)