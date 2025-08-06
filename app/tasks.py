# # app/tasks.py
# from app.extractor import extract_text_from_url
# from app.langchain_pipe import run_langchain_pipeline
# from app.celery_config import celery_app


# @celery_app.task
# def process_url_task(url: str):
#     text = extract_text_from_url(url)
#     chunk_count = run_langchain_pipeline(text)
#     return f"총 {chunk_count}개 청크 저장 완료!"
