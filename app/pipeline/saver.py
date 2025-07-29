from sqlalchemy.exc import SQLAlchemyError
from app.db.connection import SessionLocal
from app.db.models import Document
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def save_embeddings_to_db(texts: list[str], embeddings: list[list[float]]) -> None:
    session = SessionLocal()
    try:
        for content, vector in zip(texts, embeddings):
            # PostgreSQL 저장
            doc = Document(content=content, embedding=vector)
            session.add(doc)

            # Elasticsearch 저장 (float으로 형 변환)
            es.index(index="tip-index", document={
                "content": content,
                "embedding": [float(v) for v in vector]
            })

        session.commit()
        print(f"{len(texts)}개 문서 저장 완료")
    except SQLAlchemyError as e:
        session.rollback()
        raise RuntimeError(f"[DB] 저장 실패: {e}")
    finally:
        session.close()
