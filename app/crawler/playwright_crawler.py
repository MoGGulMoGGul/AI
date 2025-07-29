# Playwright 기반 JS 렌더링 대응 크롤러
# JS 기반 동적 페이지 처리용

import asyncio
from playwright.async_api import async_playwright
from .base import BaseCrawler
from .utils import clean_html


class PlaywrightCrawler(BaseCrawler):
    def crawl(self, url: str) -> str:
        return asyncio.run(self._async_crawl(url))

    async def _async_crawl(self, url: str) -> str:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=20000)
                await page.wait_for_load_state("load")

                content = await page.content()
                await browser.close()

        except Exception as e:
            raise RuntimeError(f"[Playwright] 크롤링 실패: {e}")

        # HTML → 텍스트로 변환
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator="\n")
        return clean_html(text)

def crawl_text_from_url(url: str) -> str:
    crawler = PlaywrightCrawler()
    return crawler.crawl(url)