# app/router/search.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.pipeline.embedder import embed_texts
from elasticsearch import Elasticsearch
from typing import List

router = APIRouter()

# Elasticsearch 연결
es = Elasticsearch(
    "http://localhost:9200",
    headers={
        "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
        "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"
    }
)

INDEX_NAME = "tip-index"

# 요청 스키마
class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

# 응답 스키마
class SearchResult(BaseModel):
    score: float
    content: str

class SearchResponse(BaseModel):
    results: List[SearchResult]

# 검색 API
@router.post(
    "/search/",
    summary="유사한 꿀팁 검색",
    description="입력된 질문과 유사한 꿀팁 콘텐츠를 Elasticsearch를 통해 검색합니다.",
    response_model=SearchResponse
)
def search_similar_documents(req: SearchRequest):
    try:
        # 1. 쿼리 임베딩
        query_vector_tensor = embed_texts([req.query])[0]
        query_vector = query_vector_tensor.tolist()

        # 2. Elasticsearch 벡터 유사도 검색
        response = es.search(index=INDEX_NAME, size=req.top_k, query={
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        })

        # 3. 결과 정리
        results = [
            {
                "score": hit["_score"],
                "content": hit["_source"]["content"]
            }
            for hit in response["hits"]["hits"]
        ]

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"벡터 검색 실패: {e}")
