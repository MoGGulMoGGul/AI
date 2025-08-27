# AI/app/summarizer.py 

import os
import boto3
from botocore.exceptions import NoCredentialsError
from app.celery_config import celery_app
from app.extractor import extract_text_from_url
from app.video_handler import get_combined_transcript
from app.text_filter import clean_text
from app.ai_utils import summarize_and_tag
from app.langchain_pipe import run_langchain_pipeline
import requests
from app.image_handler import process_image_tip
from app.thumbnail_handler import generate_thumbnail
import uuid

# S3 업로드 함수
def upload_to_s3(data, file_extension):
    """S3에 썸네일 데이터를 업로드하고 URL을 반환합니다."""
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name='ap-northeast-2'
        )
        bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        file_name = f"thumbnails/{uuid.uuid4()}.{file_extension}"

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data,
            ContentType=f'image/{file_extension}'
            # ACL='public-read' 옵션을 삭제하여 버킷의 기본 권한 설정을 따르도록 합니다.
        )
        
        return f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_name}"

    except NoCredentialsError:
        print("S3 자격 증명을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"S3 업로드 중 오류 발생: {e}")
        return None


@celery_app.task(name="app.summarizer.process_url_task")
def process_url_task(url: str):
    thumbnail_url = None
    try:
        # 썸네일 생성 로직은 동일
        thumbnail_raw_data, thumb_type = generate_thumbnail(url)

        if thumbnail_raw_data:
            if thumb_type == "image":
                # 생성된 썸네일(bytes)을 S3에 업로드하고 URL을 받음
                thumbnail_url = upload_to_s3(thumbnail_raw_data, "png")
            elif thumb_type == "redirect":
                # 리다이렉트 URL은 그대로 사용
                thumbnail_url = thumbnail_raw_data
    except Exception as e:
        print(f"[Error] 썸네일 처리 중 오류 발생: {e}")
        thumbnail_url = None


    try:
        headers = requests.head(url, timeout=5).headers
        content_type = headers.get("Content-Type", "")

        if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]) or "image" in content_type:
            local_filename = "temp_image.jpg"
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            result = process_image_tip(local_filename)
            return {
                "type": "이미지",
                "title": result['summary_and_tags']['title'],
                "summary": result['summary_and_tags']['summary'],
                "tags": result['summary_and_tags']['tags'],
                "thumbnail_url": thumbnail_url # 최종 썸네일 URL 반환
            }

        elif "youtube.com" in url or "youtu.be" in url:
            full_text = get_combined_transcript(url)
            cleaned_text = clean_text(full_text)
            result = summarize_and_tag(cleaned_text)
            return {
                "type": "유튜브",
                "title": result['title'],
                "summary": result['summary'],
                "tags": result['tags'],
                "thumbnail_url": thumbnail_url # 최종 썸네일 URL 반환
            }

        else:
            text = extract_text_from_url(url)
            result = run_langchain_pipeline(text)
            return {
                "type": "웹페이지",
                "title": result['title'],
                "summary": result['summary'],
                "tags": result['tags'],
                "thumbnail_url": thumbnail_url # 최종 썸네일 URL 반환
            }

    except Exception as e:
        return {
            "type": "에러",
            "title": "요약 실패",
            "summary": f"처리 실패: {e}",
            "tags": ["오류"],
            "thumbnail_url": None
        }