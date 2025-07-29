# app/crawler/__init__.py

from .bs_text_crawler import BeautifulSoupCrawler
from .playwright_crawler import PlaywrightCrawler

def crawl_text_from_url(url: str) -> str:
    # 기본 값 : BeautifulSoupCrawler
    crawler = BeautifulSoupCrawler()

    # 필요에 따라 PlaywrightCrawler로 변경 가능
    if "some-javascript-heavy-site.com" in url:
        print("[INFO] JS 렌더링 필요 → Playwright 사용")
        crawler = PlaywrightCrawler()

    return crawler.crawl(url)