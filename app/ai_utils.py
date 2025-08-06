# app/ai_utils.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_and_tag(text: str):
    prompt = (
        "다음 글을 기반으로 아래 3가지를 생성하세요:\n"
        "1. 제목 (30자 이내)\n"
        "2. 한 문단 요약\n"
        "3. 관련 태그 5개 (쉼표로 구분)\n\n"
        "출력 형식:\n"
        "[제목]\n[요약 문장]\n[태그1, 태그2, 태그3, 태그4, 태그5]\n\n"
        f"{text}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip().split("\n")

        title = result[0]
        summary = result[1] if len(result) > 1 else "요약 없음"
        tags_line = result[2] if len(result) > 2 else ""
        tags = [tag.strip() for tag in tags_line.split(",") if tag.strip()]

        return {
            "title": title,
            "summary": summary,
            "tags": tags
        }

    except Exception:
        return {
            "title": "제목 생성 실패",
            "summary": "요약 실패",
            "tags": ["실패", "에러", "요약불가", "GPT오류", "기본"]
        }