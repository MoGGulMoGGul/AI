# app/pipeline/embedder.py
# OpenAI 임베딩 API를 사용하여 텍스트를 벡터로 변환하는 기능을 구현

# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()  # .env에서 API 키 불러오기

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def embed_texts(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
#     """
#     텍스트 리스트를 OpenAI 임베딩 벡터로 변환
#     :param texts: 분할된 텍스트 조각 리스트
#     :param model: OpenAI 임베딩 모델
#     :return: 각 텍스트에 대한 임베딩 벡터 리스트
#     """
#     try:
#         response = client.embeddings.create(
#             input=texts,
#             model=model
#         )
#         return [e.embedding for e in response.data]
#     except Exception as e:
#         raise RuntimeError(f"[OpenAI] 임베딩 실패: {e}")


# Hugging Face 
from sentence_transformers import SentenceTransformer

# 무료 모델 로드
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    무료 임베딩 모델로 텍스트를 벡터로 변환
    :param texts: 텍스트 조각 리스트
    :return: 각 텍스트에 대한 벡터 리스트
    """
    return model.encode(texts, convert_to_numpy=False)  # convert_to_tensor도 가능
