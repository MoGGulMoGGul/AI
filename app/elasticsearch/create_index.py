# from elasticsearch import Elasticsearch
# from elasticsearch.exceptions import RequestError

# es = Elasticsearch("http://localhost:9200")

# INDEX_NAME = "documents"

# mapping = {
#     "mappings": {
#         "properties": {
#             "content": {"type": "text"},
#             "embedding": {
#                 "type": "dense_vector",
#                 "dims": 384,
#                 "index": False  # 일단 False로 설정해서 오류 회피
#             }
#         }
#     }
# }

# try:
#     if not es.indices.exists(index=INDEX_NAME):
#         es.indices.create(index=INDEX_NAME, body=mapping)
#         print(f"인덱스 '{INDEX_NAME}' 생성 완료!")
#     else:
#         print(f"인덱스 '{INDEX_NAME}' 이미 존재함.")
# except RequestError as e:
#     print(f"인덱스 생성 실패: {e.info}")
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

if not es.indices.exists(index="tip-index"):
    es.indices.create(
        index="tip-index",
        body={
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": 384}
                }
            }
        }
    )
    print("인덱스 생성 완료")
else:
    print("이미 존재하는 인덱스입니다.")
