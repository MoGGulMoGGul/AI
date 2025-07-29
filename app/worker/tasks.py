# app/worker/tasks.py
from app.crawler import crawl_text_from_url
from app.pipeline.splitter import split_text
from app.pipeline.embedder import embed_texts
from app.pipeline.saver import save_embeddings_to_db
from app.worker import celery_app

@celery_app.task
def process_url_task(url: str) -> str:
    print(f"[CELERY TASK] URL 처리 시작: {url}")
    try:
        print(f"[1] 크롤링 시작: {url}")
        raw_text = crawl_text_from_url(url)

        print(f"[2] 텍스트 분할 시작")
        chunks = split_text(raw_text)

        print(f"[3] 임베딩 생성 시작")
        embeddings = embed_texts(chunks)

        print(f"[4] DB 저장 시작")
        save_embeddings_to_db(chunks, embeddings)

        return f"총 {len(chunks)}개 청크 저장 완료!"
    except Exception as e:
        return f"[ERROR] 처리 실패: {str(e)}"
