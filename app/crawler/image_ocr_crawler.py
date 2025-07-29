"""
1. 이미지 URL을 받아서 다운로드
2. 회색조 변환 → 이진화(Thresholding) 처리
3. Tesseract OCR로 텍스트 추출 (lang="kor+eng")
4. 결과 문자열 반환
"""

import requests
from bs4 import BeautifulSoup
from PIL import Image # 이미지 처리 라이브러리 -> 이미지 파일을 파이썬 객체로 열거나 저장하는 조작 클래스
from io import BytesIO # 바이트 스트림을 처리하기 위한 모듈 -> 바이트 데이터를 메모리에서 읽고 쓸 수 있게 해줌(이진 데이터를 파일처럼 다룰 수 있게 해줌)
import pytesseract
import numpy as np
import cv2

from .base import BaseCrawler
from .utils import clean_html
from urllib.parse import urljoin

class ImageOCRCrawler(BaseCrawler):
    def crawl(self, url: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"[ImageOCRCrawler] 요청 실패: {e}")

        soup = BeautifulSoup(response.content, "html.parser")
        ocr_texts = []

        for img in soup.find_all("img"):
            img_url = img.get("src")
            if not img_url:
                continue

            # 상대 경로 처리
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif img_url.startswith("/"):
                img_url = urljoin(url, img_url)

            try:
                img_res = requests.get(img_url, timeout=5)
                image = Image.open(BytesIO(img_res.content)).convert("L")  # 회색조

                # 이진화 (thresholding)
                img_np = np.array(image)
                _, thresh = cv2.threshold(img_np, 150, 255, cv2.THRESH_BINARY)
                processed_img = Image.fromarray(thresh)

                # OCR 수행
                ocr_result = pytesseract.image_to_string(processed_img, lang="kor+eng")

                if ocr_result.strip():
                    ocr_texts.append(ocr_result)
            except Exception as e:
                print(f"OCR 처리 중 에러: {e}")
                continue

        return clean_html("\n\n".join(ocr_texts))