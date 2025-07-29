# app/image_worker/tasks.py
from app.crawler.image_ocr_crawler import ImageOCRCrawler
from app.pipeline.splitter import split_text
from app.pipeline.embedder import embed_texts
from app.pipeline.saver import save_embeddings_to_db
from app.image_worker.celery import celery_app

@celery_app.task
def process_image_url_task(url: str) -> str:
    print(f"[CELERY TASK] 이미지 URL 처리 시작: {url}")
    try:
        crawler = ImageOCRCrawler()
        raw_text = crawler.crawl(url)

        chunks = split_text(raw_text)
        embeddings = embed_texts(chunks)
        save_embeddings_to_db(chunks, embeddings)

        return f"[완료] 총 {len(chunks)}개 청크 저장"
    except Exception as e:
        return f"[ERROR] 처리 실패: {str(e)}"
