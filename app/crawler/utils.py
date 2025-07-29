# HTML 정제, 유틸 함수
# HTML 정리, 정규식 제거, 텍스트 필터링 등
import re

def clean_html(text: str) -> str:
    text = re.sub(r'\s+', '', text)  # 연속된 공백 제거
    text = re.sub(r'[\r\n\t]+', '\n', text) # 줄바꿈, 탭 제거
    return text.strip()  # 앞뒤 공백 제거