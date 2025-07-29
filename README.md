# AI
[모꿀모꿀] 모꿀모꿀 서비스의 AI 레포지토리

- 사용언어 Python

## 명령어 모음
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

- requirements.txt 업데이트
```
    pip freeze > requirements.txt
```

- FastAPI 실행 명령어(터미널 1)
```
    uvicorn app.main:app --reload
```

- vscode 기준(가상 환경 실행 명령어)
```
    .\venv\Scripts\activate
```

- celery 실행 명령어(터미널 2)
    - pool=solo는 윈도우에서 실행 시 안전하게 실행가능
```
    celery -A app.worker.celery.celery_app worker --loglevel=info --pool=solo
```


### Swagger 주소
- http://127.0.0.1:8000/docs#/