# =====================================================================
# Stage 1: Builder - 의존성 설치를 위한 단계
# =====================================================================
FROM python:3.11-slim as builder

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# 가상 환경 생성
RUN python -m venv /opt/venv

# 가상 환경의 pip를 사용하도록 환경 변수 설정
ENV PATH="/opt/venv/bin:$PATH"

# requirements.txt 복사 및 의존성 설치 (캐시 활용을 위해 분리)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN python -m playwright install chromium

# =====================================================================
# Stage 2: Final Base Image - 실제 실행을 위한 최종 이미지
# =====================================================================
FROM python:3.11-slim

# 필수 런타임 시스템 패키지 및 Playwright 의존성 수동 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    # Playwright 실행에 필요한 라이브러리들
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2 \
  && rm -rf /var/lib/apt/lists/*

# Builder 단계에서 설치한 가상 환경 복사
COPY --from=builder /opt/venv /opt/venv
# Builder 단계에서 설치한 Playwright 브라우저 복사
COPY --from=builder /ms-playwright /ms-playwright

# 환경 변수 설정
ENV PATH="/opt/venv/bin:$PATH"
ENV PLAYWRIGHT_BROWSERS_PATH="/ms-playwright"

# 작업 디렉토리 설정
WORKDIR /app

# 이 이미지는 기본 이미지이므로 CMD를 지정하지 않습니다.
# 각 서비스(web, celery)가 CMD를 오버라이드하여 사용합니다.
