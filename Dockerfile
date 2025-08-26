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

# =====================================================================
# Stage 2: Final - 실제 실행을 위한 최종 이미지
# =====================================================================
FROM python:3.11-slim

# 필수 런타임 시스템 패키지만 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Builder 단계에서 설치한 가상 환경 복사
COPY --from=builder /opt/venv /opt/venv

# 가상 환경을 사용하도록 환경 변수 설정
ENV PATH="/opt/venv/bin:$PATH"

# Playwright 브라우저 설치
# RUN python -m playwright install chromium # 이 부분은 시간이 매우 오래 걸릴 수 있으므로,
# 만약 문제가 지속되면 아래 Dockerfile.playwright 이미지를 사용하는 것을 고려
RUN python -m playwright install --with-deps chromium

# 애플리케이션 소스 코드 복사
COPY ./app ./app

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
