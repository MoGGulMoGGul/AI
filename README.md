# AI
[모꿀모꿀] 모꿀모꿀 서비스의 AI 레포지토리

- 사용언어 Python
- install 명령어 
```
    pip install -r requirements.txt
```

- .env 예시
```
    # .env.example
    OPENAI_API_KEY=your-api-key
    DATABASE_URL=your-db-url
```

-----------

taskkill /F /IM python.exe
uvicorn app.main:app

docker exec -it momo_postgres psql -U user -d momo
-- ① pgvector 확장 설치 확인
\dx

-- ② tip_data 테이블 생성 여부 확인
\dt

-- ③ 데이터 유무 확인 (없어도 됨)
SELECT * FROM tip_data;

 ️ 전체 SQL 코드 정리
1. 현재 데이터베이스에 있는 테이블 목록 확인

\dt

PostgreSQL의 메타 명령어
결과: langchain_pg_collection, langchain_pg_embedding, tip_data 등

2. 테이블 구조(컬럼 정보) 확인
\d langchain_pg_embedding

각 컬럼의 이름, 타입 확인 (예: collection_id, embedding, document, ...)

\d langchain_pg_collection

3. LangChain이 만든 컬렉션 이름 확인

SELECT * FROM langchain_pg_collection;

컬럼명     설명
name    컬렉션 이름 (tip_data 등)
uuid    이 컬렉션을 식별하는 LangChain 내부용 ID

4. 컬렉션 ID별로 벡터(문서) 저장 확인
🔹 전체 문서 확인

SELECT document FROM langchain_pg_embedding LIMIT 5;

🔹 특정 컬렉션(tip_data)에 해당하는 문서만 보기
(컬렉션 UUID가 예: 6e30ae0f-49fd-4ddc-93f5-f5650a07ff1c일 때)

SELECT document FROM langchain_pg_embedding
WHERE collection_id = '6e30ae0f-49fd-4ddc-93f5-f5650a07ff1c';

5. 저장된 임베딩 벡터 수 세기

SELECT COUNT(*) FROM langchain_pg_embedding;
→ 벡터가 몇 개 저장되었는지 확인

6. 수동 생성된 tip_data 테이블 확인

SELECT * FROM tip_data;

❗ LangChain이 사용하는 테이블은 아님 (도커 초기 설정에서 생성한 샘플 테이블)

보너스: 데이터 삭제용

-- 특정 컬렉션에 해당하는 모든 벡터 삭제
DELETE FROM langchain_pg_embedding
WHERE collection_id = '6e30ae0f-49fd-4ddc-93f5-f5650a07ff1c';

-- 컬렉션 자체 삭제
DELETE FROM langchain_pg_collection
WHERE uuid = '6e30ae0f-49fd-4ddc-93f5-f5650a07ff1c';

-----------------

# 가상환경 생성
```
python -m venv .venv
```

# 가상환경 활성화 (Windows)
```
.\.venv\Scripts\activate
```

# 의존성 설치
```
pip install --upgrade pip
pip install -r requirements.txt
```

# ffmpeg 설치 (YouTube 오디오 추출용)
- 관리자 권한 PowerShell에서 실행
```
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install ffmpeg -y
```

- 경로 확인 명령어
```
Get-Command ffmpeg
```

- 수동 경로 등록 필요
    - video_handler.py에서 44번째 줄 'ffmpeg_location': 'C:/ProgramData/chocolatey/bin',
    - C:/ProgramData/chocolatey/bin 이 부분 개인 경로 등록 필요


# docker 설치 명령어 
- docker 전체 서비스 실행
```
docker-compose up -d
```

- docker 접속 명령어
```
docker exec -it momo_postgres psql -U user -d momo
```

- docker desktop에서 postgreSQL 접속 명령어
```
psql -U user -d momo 
```

# FastAPI 서버 실행
```
uvicorn app.main:app --reload
```

# Celery 워커 실행 (Windows 안정화 옵션 포함)
```
celery -A app.celery_config.celery_app worker --loglevel=info --pool=solo
```

# 테스트 주소
- http://127.0.0.1:8000/docs
- /async-index/ : 텍스트, 이미지, 영상 한 번에 가능함

