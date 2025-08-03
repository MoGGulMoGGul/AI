# ▶️ Python 3.11 slim 이미지 기반
FROM python:3.11-slim

# ▶️ 작업 디렉토리 설정
WORKDIR /app

# ▶️ 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ▶️ 전체 소스 코드 복사
COPY ./app ./app

# ▶️ 포트 개방 (FastAPI용)
EXPOSE 8000

# ▶️ 기본 실행 명령 (FastAPI 서버 실행용)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
