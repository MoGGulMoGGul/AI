# app/summarizer.py
from openai import OpenAI
import os

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_and_tag(text: str):
    prompt = f"다음 글을 한 문단으로 요약하고, 관련 태그 5개 추출:\n\n{text}"
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    return result
