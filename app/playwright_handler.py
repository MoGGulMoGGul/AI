# app/playwright_handler.py
from playwright.sync_api import sync_playwright

def extract_html_with_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=10000)
        page.wait_for_timeout(2000)  # JS 로딩 대기

        html = page.content()
        browser.close()
        return html
