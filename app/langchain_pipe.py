# app/langchain_pipe.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()

def run_langchain_pipeline(raw_text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([raw_text])

    # ✅ API 키 기반 OpenAI Embedding 사용
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    vectorstore = PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="tip_data",
        connection_string=os.getenv("DB_URL")
    )

    return len(docs)
