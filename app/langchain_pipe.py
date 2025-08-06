# app/langchain_pipe.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings

from app.elasticsearch_client import index_tip_document  # ✅ Elasticsearch 연동 추가
from app.ai_utils import summarize_and_tag  # ✅ ai_utils로 이동된 요약 및 태그 함수 사용

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
        collection_name="tip_data",  # 👉 필요시 컬렉션명도 변경 가능
        connection_string=os.getenv("PGVECTOR_CONNECTION_STRING")
    )

    # 4️⃣ Elasticsearch에 제목 + 요약 + 태그 저장
    summary = ""
    tag_list = []
    try:
        summary_and_tags = summarize_and_tag(raw_text)
        summary = summary_and_tags["summary"]
        title = summary_and_tags["title"]
        tag_list = summary_and_tags["tags"]

        index_tip_document(text=raw_text, summary=summary, tags=tag_list)
    except Exception as e:
        print(f"[Elasticsearch 저장 중 오류] {e}")

    return {
        "chunks": len(docs),
        "title": title,
        "summary": summary,
        "tags": tag_list
    }
