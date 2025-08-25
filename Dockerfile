# AI/Dockerfile

# Python 3.11 slim 이미지 기반
FROM python:3.11-slim

# 필수 시스템 패키지 (cv2/EasyOCR/Playwright/yt_dlp용)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 libxext6 libxrender1 \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# 파이썬 의존성
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저(Chromium) 설치 (수정된 부분)
# 문제가 되는 --with-deps 옵션을 제거합니다.
RUN python -m playwright install chromium

# 앱 소스
COPY ./app ./app

# 포트
EXPOSE 8000

# 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]