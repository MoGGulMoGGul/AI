# AI/app/elasticsearch_client.py (파일 전체를 아래 코드로 교체)

import os
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, TransportError

ES_URL = os.getenv("ES_URL", "http://elasticsearch:9200")
es = None
try:
    # 프로그램 시작 시 한 번만 연결 시도
    es_client = Elasticsearch(ES_URL, timeout=5)
    if es_client.ping():
        es = es_client
        print("[Elasticsearch] 연결 성공")
except ConnectionError:
    print("[Elasticsearch] 연결 실패. Elasticsearch 관련 기능이 비활성화됩니다.")


def create_index_if_not_exists(index_name="tips"):
    if not es: return
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
    except (ConnectionError, TransportError) as e:
        print(f"[Elasticsearch 연결 오류] {e}")


def index_tip_document(text: str, summary: str, tags: list, index_name="tips"):
    if not es: return
    try:
        doc = {"text": text, "summary": summary, "tags": tags}
        es.index(index=index_name, document=doc)
    except Exception as e:
        print(f"[Elasticsearch 저장 오류] {e}")


def search_by_tag(tag: str, index_name="tips"):
    if not es: return []
    try:
        response = es.search(
            index=index_name,
            query={"match": {"tags": tag}}
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"[Elasticsearch 검색 오류] {e}")
        return []