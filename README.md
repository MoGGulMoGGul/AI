# 모꿀모꿀 (MoggulMoggul) - AI 서비스
![header](https://capsule-render.vercel.app/api?type=cylinder&color=EAC149&height=130&section=header&text=MOGGUL-MOGGUL%20AI&fontSize=55&animation=scaleIn&fontColor=FFF)

<p align="center">
  <img src="https://img.shields.io/badge/python-3776AB.svg?&style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/fastapi-%23009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/docker-%232496ED.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/openai-%23412991.svg?&style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/langchain-%232D69A4.svg?&style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/pytorch-%23EE4C2C.svg?&style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/playwright-%232EAD33.svg?&style=for-the-badge&logo=playwright&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/postgresql-%234169E1.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/redis-%23DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/amazon s3-%23569A31.svg?&style=for-the-badge&logo=amazons3&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon EC2-%23FF9900.svg?&style=for-the-badge&logo=amazon-ec2&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon RDS-%23527FFF.svg?&style=for-the-badge&logo=amazon-rds&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon ElastiCache-%23FF9900.svg?&style=for-the-badge&logo=amazon-elasticache&logoColor=white"/>
  <br>
</p>

---

----
## 프로젝트 개요
웹페이지, 유튜브, 이미지 등 다양한 형태의 온라인 콘텐츠를 자동으로 분석하여 제목, 요약, 태그, 썸네일을 생성하고, 처리된 데이터를 백엔드 서버에 제공하는 비동기 콘텐츠 처리 AI 서비스 입니다.

## 팀원 소개
| **이름** | **역할**        | **GitHub**                   |
|--------|---------------|------------------------------|
| 구강현    | 백엔드 / 배포 / AI | https://github.com/GangHyoun |
| 송보민    | 백엔드 / AI      | https://github.com/Songbomin |
| 정혜지    | 프론트엔드 / 디자인        | https://github.com/heartggs  |

----

## 프로젝트 구성

### 주요 기능
- **비동기 콘텐츠 처리**: Celery를 사용하여 URL(웹페이지, 유튜브, 이미지)을 비동기적으로 처리하여 메인 서버의 부하를 줄입니다.
- **다양한 콘텐츠 요약 및 태깅**:
    - **웹페이지**: 동적/정적 웹페이지의 본문을 추출(`Playwright`, `BeautifulSoup`)하고 `OpenAI`를 통해 요약 및 태그를 생성합니다.
    - **유튜브**: 영상의 자막과 음성을 `Whisper`로 추출하여 텍스트로 변환한 후 요약 및 태그를 생성합니다.
    - **이미지**: `EasyOCR`로 이미지 내 텍스트를 추출(OCR)하여 요약 및 태그를 생성합니다.
- **썸네일 자동 생성**:
    - `Playwright`를 사용하여 웹페이지의 스크린샷을 찍거나, 유튜브/이미지 URL에서 직접 썸네일을 추출합니다.
    - 생성된 썸네일은 **AWS S3**에 업로드되어 URL로 관리됩니다.
- **벡터 데이터베이스 활용**: LangChain 파이프라인을 통해 처리된 텍스트를 벡터로 변환하고 **PGVector**에 저장하여 추후 검색 및 활용 가능성을 열어둡니다.

## 툴체인 & 프레임워크

### 프레임워크

| 분류 | 사용 기술 | 설명 |
|---|---|---|
| **언어** | Python 3.10+ | AI 모델링 및 비동기 처리를 위한 주력 개발 언어 |
| **웹 프레임워크** | FastAPI | 비동기 API 서버를 구축하여 높은 성능과 빠른 응답 속도 보장 |
| **비동기 작업 큐** | Celery with Redis | URL 콘텐츠 처리 작업을 비동기적으로 실행하여 메인 서버 부하 감소 |
| **AI/ML** | OpenAI, LangChain | 텍스트 요약, 태그 생성 등 자연어 처리 파이프라인 구축 |
| **AI/ML** | Whisper, EasyOCR | 유튜브 음성 및 이미지 내 텍스트를 추출하여 데이터 소스 확장 |
| **웹 스크래핑** | Playwright, BeautifulSoup | 동적/정적 웹페이지의 본문 콘텐츠를 정확하게 추출 |
| **데이터베이스** | PostgreSQL with PGVector | 텍스트 벡터 데이터를 저장하여 향후 검색 및 AI 기능 확장성 확보 |
| **클라우드 서비스** | AWS S3 | 생성된 썸네일 이미지를 안정적으로 저장하고 URL로 관리 |

### 툴체인

| 분류 | 사용 기술 | 설명 |
|---|---|---|
| **IDE** | Visual Studio Code | Python 개발 및 디버깅에 최적화된 통합 개발 환경 |
| **패키지 매니저** | Pip | `requirements.txt`를 통해 Python 프로젝트 의존성 관리 |
| **컨테이너화** | Docker, Docker Compose | 개발 환경을 컨테이너화하여 일관된 배포 및 실행 환경 보장 |
| **버전 관리** | Git + GitHub | 소스 코드 버전 관리 및 팀 협업을 위한 플랫폼 |
| **CI/CD** | GitHub Actions | main 브랜치 push 시 Docker 이미지를 빌드하여 EC2에 자동 배포 |
| **배포** | AWS EC2 | Docker 컨테이너를 이용한 서비스 애플리케이션 배포 환경 |
| **테스트 도구** | Postman | FastAPI로 구축된 API 엔드포인트 테스트 및 명세 확인 |
| **런타임 환경** | Python 3.10+ | AI 서비스 애플리케이션 실행 환경 |
| **인프라 관리** | AWS Console | EC2, RDS, S3 등 클라우드 인프라 구성 및 모니터링 |

---

## 프로젝트 프로그램 설치방법

### 사전 요구사항
- **Docker** 및 **Docker Compose** 설치
- **AWS S3** 버킷 및 IAM 자격 증명
- **OpenAI API Key**
- **PostgreSQL** 데이터베이스 (로컬 또는 원격)

### 설치 과정
1. **프로젝트 클론**
   ```bash
   git clone [https://github.com/your-username/moggulmoggul-ai.git](https://github.com/your-username/moggulmoggul-ai.git)
   cd moggulmoggul-ai
    ```
2. **.env 파일 설정**
   # OpenAI API 설정
    ```
    OPENAI_API_KEY="sk-..."
    ```

    # PostgreSQL 연결 정보 (Docker Compose 내부 네트워크 기준)
    ```
    POSTGRES_DB=momo
    POSTGRES_USER=user
    POSTGRES_PASSWORD=p1234
    PGVECTOR_CONNECTION_STRING=postgresql+psycopg2://user:p1234@db:5432/momo
    ```

    # Redis 연결 정보 (Docker Compose 내부 네트워크 기준)
    ```
    REDIS_URL=redis://redis:6379/0
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    ```

    # AWS S3 자격 증명
    ```
    AWS_ACCESS_KEY_ID="your_access_key"
    AWS_SECRET_ACCESS_KEY="your_secret_key"
    AWS_S3_BUCKET_NAME="your_bucket_name"
    ```

3. **Docker 이미지 빌드 및 컨테이너 실행**
    ```
    docker-compose up --build
    ```

----

### 프로그램 사용법
1. **애플리케이션 실행 확인**
<br/>
Docker 컨테이너가 정상적으로 실행되면, FastAPI 웹 서버는 http://localhost:8000에서 접근할 수 있습니다.

2. **API 엔드 포인트**
- 비동기 요약 작업 생성: `POST` `/async-index/`
    - Request Body: `{"url": "요약할 URL"}`
    - Response: `{"task_id": "생성된 작업 ID"}`

- 작업 상태 및 결과 조회: `GET` `/summary-result/{task_id}`
    - Response (완료 시):
        ```
        {
            "summary": "생성된 요약 내용",
            "title": "생성된 제목",
            "tags": ["태그1", "태그2"],
            "thumbnail_url": "S3에 업로드된 썸네일 URL"
        }
        ```
    - Response (진행 중) : `HTTP 202 Accepted` 상태 코드와 함께 진행 중 메시지 반환
- 썸네일 생성: `POST` `/thumbnail`

    - Request Body: `{"url": "썸네일 생성할 URL"}`

    - Response: 생성된 썸네일 이미지(PNG) 또는 유튜브 썸네일 URL로 리다이렉트

API 테스트는 Postman과 같은 도구를 사용하거나 FastAPI에서 제공하는 Swagger UI (http://localhost:8000/docs)를 통해 할 수 있습니다.

---

## API 명세서

| Method | Path | 설명 | 요청 바디 (요약) | 응답 (요약) | 비고 |
|---|---|---|---|---|---|
| POST | `/extract` | URL 본문 추출 | `{ "url": "https://..." }` | `{ "text": "<정제된 본문>" }` | 정적 실패 시 Playwright로 재시도 |
| POST | `/extract-image-tip` | 이미지 OCR → 정제 → 요약·태그 | `multipart/form-data` (`file`) | `{ raw_text, cleaned_text, title, summary, tags }` | EasyOCR 사용 |
| POST | `/extract-video-tip` | YouTube 자막+Whisper 병합 → 정제 → 요약·태그 | `{ "url": "https://youtu..." }` | `{ raw_text, cleaned_text, title, summary, tags }` | yt-dlp+ffmpeg, Whisper(base) |
| POST | `/index-tip` | 텍스트 → 청크 → 임베딩 저장 → ES 색인 | `{ "text": "..." }` | `{ message, title, tags }` | pgvector(PSQL) + OpenAIEmbeddings |
| POST | `/async-index/` | URL 비동기 처리 태스크 생성 | `{ "url": "https://..." }` | `{ "task_id": "<id>" }` | Celery 태스크 `app.summarizer.process_url_task` |
| GET | `/task-status/{task_id}` | 태스크 상태/부분결과 | - | `{ status, result? }` | `result`는 준비 시에만 포함 |
| GET | `/summary-result/{task_id}` | 비동기 요약 최종 결과 | - | `{ title, summary, tags, thumbnail_data, thumbnail_type }` | **미완료 시 `202 Accepted`** |
| GET | `/search-tag` | ES 태그 검색 | `?tag=키워드` | `[{ text, summary, tags, ... }]` | 인덱스 `tips` |
| POST | `/thumbnail` | URL 타입별 썸네일 생성 | `{ "url": "..." }` | `image/png`(바이트) | YouTube/이미지/웹 모두 PNG 바이트 |
| POST | `/qa` | RAG Q&A (pgvector 검색 + LLM) | `{ "query": "..." }` | `{ matched_chunks, answer?, sources? }` | `OPENAI_API_KEY` 필요 |


---

## 파이프라인 

### 1) 웹페이지(URL) → 본문 추출
- `requests.get`으로 HTML 획득 → `structure_detector.extract_main_content_from_html`
- 본문이 부족/실패하면 **Playwright 렌더링** 후 다시 본문 추출
- 후처리: `text_filter.clean_text` (공백/잡음 제거)

### 2) 유튜브(URL) → 텍스트화
- `youtube_transcript_api`로 자막(ko/en) 시도 → 실패 시 빈 리스트
- `yt-dlp` + `FFmpegExtractAudio`로 오디오(mp3) 추출 → `Whisper(base)`로 전사
- `rapidfuzz`로 **자막 vs Whisper** 중복/유사 구간 제거 및 병합
- `"[유튜브 자막 기반]" + 자막 + "[Whisper에서 잡힌 추가 내용]"` 형태로 합본
- 후처리: `text_filter.clean_text`

### 3) 이미지(file/URL) → 텍스트화
- `EasyOCR(ko,en)`로 OCR → 줄 결합/정제 → `text_filter.clean_text`

### 4) 요약·태깅 (공통)
- `ai_utils.summarize_and_tag` (LLM: `gpt-3.5-turbo` 등)
- 출력 스키마: `{ title, summary, tags[최대 5] }` (실패 시 기본 메시지 제공)

### 5) 썸네일 생성 (비동기 태스크 내)
- `thumbnail_handler.generate_thumbnail`
  - **YouTube**: 고화질 썸네일 다운로드 → PNG 바이트
  - **이미지 URL**: 원본 리사이즈/패딩 → PNG 바이트
  - **일반 웹**: Playwright 스크린샷 → PNG 바이트
- 결과는 **Base64 + MIME**로 `summary-result`에 포함: `thumbnail_data`, `thumbnail_type`


---

## 임베딩/검색 스택

### 벡터 스토어 (pgvector, PostgreSQL)
- **청크 전략:** `chunk_size = 500`, `chunk_overlap = 50`
- **컬렉션:** `tip_data`
- **임베딩:** `OpenAIEmbeddings` (env: `OPENAI_API_KEY`)
- **커넥션 문자열 우선순위:** `PGVECTOR_CONNECTION_STRING` → (없으면) `DB_URL`
- **저장 플로우:** `PGVector.from_documents(docs, collection_name="tip_data", ...)`

### RAG Q&A
- **Retriever:** `PGVector(..., connection_string=DB_URL).as_retriever()`
- **LLM:** `ChatOpenAI(model="gpt-3.5-turbo", temperature=0)`
- **응답:** 관련 청크(`matched_chunks`)와 선택적 `answer`, `sources`

### Elasticsearch (키워드/태그 색인·검색)
- **ES_URL:** `http://elasticsearch:9200` (env `ES_URL`)
- **인덱스:** `tips`
- **저장 문서:** `{ text, summary, tags }`
- **검색:** `match`/`multi_match` 기반 태그 키워드 검색
- **주의:** 색인 생성 유틸 실행(존재하지 않으면 생성) 후 사용 권장


---

## 비동기 처리 (Celery)

- **Broker/Backend:** `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` (기본: `redis://redis:6379/0`)
- **태스크 디스커버리:** `celery_app.autodiscover_tasks(["app"])`
- **레이트 리밋:** `app.summarizer.process_url_task` → `10/m` (남용 방지)
- **워커 설정 팁:**
  - 타임존: `Asia/Seoul`, 직렬화: `json`
  - 동시성: 콘텐츠 길이/Whisper 사용률에 맞게 `--concurrency` 조정
  - 큐 분리(선택): `short`/`long` 큐로 URL 길이나 타입에 따라 라우팅
- **동작 흐름:**
  1) `POST /async-index/` → `{ "task_id": "..." }`
  2) `GET /task-status/{task_id}`로 진행 확인
  3) `GET /summary-result/{task_id}`로 최종 결과 수신 (**미완료 시 202**)
- **장애 대응:**
  - 재시도 정책/타임아웃 설정 권장
  - 실패 로그에 원인(URL 접근/Playwright/ffmpeg/Whisper/LLM) 명시

---

## 유튜브/오디오 관련 전제 조건

- **ffmpeg 필수:** `yt-dlp`가 `FFmpegExtractAudio` postprocessor를 사용
- **Whisper 모델:** `whisper.load_model("base")` 기준 (GPU 없으면 CPU 전사, 시간 증가)
- **자막 API:** `youtube_transcript_api`(ko/en 모두 시도). 자막이 없으면 Whisper만 활용
- **URL 처리:** `normalize_youtube_url`, `extract_video_id` 등으로 안정적 ID 추출
- **성능 팁:**
  - 긴 영상은 비동기 큐로 분리/레이트리밋 상향 조정
  - 캐시 가능한 자막은 저장 후 재사용


---
## 프로젝트 URL
- **Main** : https://github.com/MoGGulMoGGul
- **FrontEnd** : https://github.com/MoGGulMoGGul/Frontend
- **BackEnd** : https://github.com/MoGGulMoGGul/Backend
- **AI** : https://github.com/MoGGulMoGGul/AI/tree/main