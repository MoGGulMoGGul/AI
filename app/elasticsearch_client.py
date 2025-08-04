# app/elasticsearch_client.py

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, TransportError

# 🔌 Elasticsearch 클라이언트 연결
es = Elasticsearch("http://localhost:9200")

# ✅ 인덱스 존재하지 않으면 생성
def create_index_if_not_exists(index_name="tips"):
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
    except (ConnectionError, TransportError) as e:
        print(f"[Elasticsearch 연결 오류] {e}")
        raise

# ✅ 문서 인덱싱 함수
def index_tip_document(text: str, summary: str, tags: list, index_name="tips"):
    try:
        doc = {
            "text": text,
            "summary": summary,
            "tags": tags
        }
        es.index(index=index_name, document=doc)
    except Exception as e:
        print(f"[Elasticsearch 저장 오류] {e}")
        raise

# ✅ 태그로 검색하는 함수
def search_by_tag(tag: str, index_name="tips"):
    try:
        response = es.search(
            index=index_name,
            query={
                "match": {
                    "tags": tag
                }
            }
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"[Elasticsearch 검색 오류] {e}")
        return []
