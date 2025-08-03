# app/text_filter.py
def clean_text(raw_text: str) -> str:
    keywords = [
        "공감", "댓글", "MY메뉴", "URL복사", "이웃", "신고하기",
        "블로그", "카테고리", "게시판", "프로필", "공유", "폰트 크기 조정", "이야기스트", "닫기"
    ]

    lines = raw_text.splitlines()
    filtered = [line for line in lines if not any(k in line for k in keywords)]
    return "\n".join(filtered)
