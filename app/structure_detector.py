# app/structure_detector.py
from bs4 import BeautifulSoup
from unstructured.partition.html import partition_html

def extract_main_content_from_html(html: str) -> str:
    try:
        # Step 1: unstructured 사용
        elements = partition_html(text=html)
        text = "\n".join(el.text for el in elements if el.text.strip())
        if len(text) > 100:
            return text
    except Exception:
        pass

    # Step 2: fallback - 가장 긴 div/p 블록
    soup = BeautifulSoup(html, 'html.parser')
    candidates = soup.find_all(['div', 'article', 'section', 'main'])

    max_block = max(
        candidates,
        key=lambda tag: len(tag.get_text(strip=True)),
        default=None
    )

    return max_block.get_text(separator='\n', strip=True) if max_block else None
