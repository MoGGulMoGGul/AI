# app/qa_api.py
from fastapi import APIRouter
from pydantic import BaseModel
import os
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

router = APIRouter()

class QARequest(BaseModel):
    query: str

@router.post("/qa")
def qa_endpoint(request: QARequest):
    # ✅ 유사 문서 검색기 구성 (OpenAI Embedding 사용)
    retriever = PGVector(
        collection_name="tip_data",
        connection_string=os.getenv("DB_URL"),
        embedding_function=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    ).as_retriever()

    # ✅ 관련 문서 검색
    docs = retriever.get_relevant_documents(request.query)

    result = {
        "matched_chunks": [doc.page_content for doc in docs]
    }

    # ✅ GPT 기반 Q&A 응답
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        llm = ChatOpenAI(openai_api_key=openai_key, model_name="gpt-3.5-turbo", temperature=0)
        chain = load_qa_with_sources_chain(llm, chain_type="stuff")
        chain_result = chain.invoke({"input_documents": docs, "question": request.query})
        result["answer"] = chain_result["answer"]
        result["sources"] = chain_result.get("sources", "unknown")

    return result
