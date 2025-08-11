# app/elasticsearch_client.py
import os
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, TransportError

ES_URL = os.getenv("ES_URL", "http://elasticsearch:9200")
es = Elasticsearch(ES_URL)

def create_index_if_not_exists(index_name="tips"):
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
    except (ConnectionError, TransportError) as e:
        print(f"[Elasticsearch 연결 오류] {e}")
        raise

def index_tip_document(text: str, summary: str, tags: list, index_name="tips"):
    try:
        doc = {"text": text, "summary": summary, "tags": tags}
        es.index(index=index_name, document=doc)
    except Exception as e:
        print(f"[Elasticsearch 저장 오류] {e}")
        raise

def search_by_tag(tag: str, index_name="tips"):
    try:
        response = es.search(
            index=index_name,
            query={"match": {"tags": tag}}
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"[Elasticsearch 검색 오류] {e}")
        return []
