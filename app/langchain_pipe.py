# app/langchain_pipe.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings

from app.elasticsearch_client import index_tip_document  # ✅ Elasticsearch 연동 추가
from app.summarizer import summarize_and_tag  # ✅ 요약 및 태그 추출 함수

load_dotenv()

def run_langchain_pipeline(raw_text: str):
    # 1️⃣ 텍스트 쪼개기
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([raw_text])

    # 2️⃣ 벡터화
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 3️⃣ pgvector 저장
    vectorstore = PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="tip_data",
        connection_string=os.getenv("DB_URL")
    )

    # 4️⃣ Elasticsearch에 원본 텍스트 + 요약 + 태그 저장
    try:
        summary_and_tags = summarize_and_tag(raw_text)  # 한 문단 요약 + 태그 추출
        summary, *tags = summary_and_tags.split("\n")   # ✅ 가정: 요약\n태그1, 태그2,... 형식
        tag_list = [tag.strip() for tag in tags[0].split(",")] if tags else []

        index_tip_document(text=raw_text, summary=summary, tags=tag_list)
    except Exception as e:
        print(f"[Elasticsearch 저장 중 오류] {e}")

    return len(docs)
