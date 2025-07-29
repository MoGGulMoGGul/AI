# app/pipeline/splitter.py

# RecursiveCharacterTextSplitter
# 긴 텍스트를 LLM 처리 가능한 크기로 분할하는 기능을 제공 [문단(\n\n) → 줄바꿈(\n) → 마침표(.) → 공백 → 문자 순으로 스마트하게 분할]
# 자연스러운 문맥 유지 + 토큰 단위 초과 방지
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(content: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    긴 텍스트를 LLM 처리 가능한 크기로 분할함
    :param content: 크롤링된 전체 텍스트
    :param chunk_size: 각 조각의 최대 길이 (default: 500 tokens 기준)
    :param chunk_overlap: 조각 간 겹침 길이 (default: 50)
    :return: 분할된 텍스트 조각 리스트
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_text(content)
    return chunks
