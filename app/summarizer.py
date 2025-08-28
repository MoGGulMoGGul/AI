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
        )
        
        return f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_name}"

    except NoCredentialsError:
        print("S3 자격 증명을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"S3 업로드 중 오류 발생: {e}")
        return None


# Celery Task
@celery_app.task(name="app.summarizer.process_url_task")
def process_url_task(url: str, tip_id: int):
    thumbnail_url = None
    try:
        thumbnail_raw_data, thumb_type = generate_thumbnail(url)
        if thumbnail_raw_data:
            if thumb_type == "image":
                thumbnail_url = upload_to_s3(thumbnail_raw_data, "png")
            elif thumb_type == "redirect":
                thumbnail_url = thumbnail_raw_data
    except Exception as e:
        print(f"[Error] 썸네일 처리 중 오류 발생: {e}")
        thumbnail_url = None

    result = {}
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
            
            image_result = process_image_tip(local_filename)
            result = {
                "type": "이미지",
                "title": image_result['summary_and_tags']['title'],
                "summary": image_result['summary_and_tags']['summary'],
                "tags": image_result['summary_and_tags']['tags'],
                "thumbnail_url": thumbnail_url
            }

        elif "youtube.com" in url or "youtu.be" in url:
            full_text = get_combined_transcript(url)
            cleaned_text = clean_text(full_text)
            yt_result = summarize_and_tag(cleaned_text)
            result = {
                "type": "유튜브",
                "title": yt_result['title'],
                "summary": yt_result['summary'],
                "tags": yt_result['tags'],
                "thumbnail_url": thumbnail_url
            }

        else:
            text = extract_text_from_url(url)
            web_result = run_langchain_pipeline(text)
            result = {
                "type": "웹페이지",
                "title": web_result['title'],
                "summary": web_result['summary'],
                "tags": web_result['tags'],
                "thumbnail_url": thumbnail_url
            }

    except Exception as e:
        result = {
            "type": "에러",
            "title": "요약 실패",
            "summary": f"처리 실패: {e}",
            "tags": ["오류"],
            "thumbnail_url": None
        }

    # AI 작업 완료 후 Spring Boot 서버로 콜백 전송
    spring_boot_public_ip = os.getenv("SPRING_BOOT_PUBLIC_IP")
    if not spring_boot_public_ip:
        print(f"[에러] 콜백 실패: SPRING_BOOT_PUBLIC_IP 환경 변수가 설정되지 않았습니다. (tip_id: {tip_id})")
        return result

    try:
        # 환경 변수에서 읽어온 스프링 부트 서버의 공인 IP 주소를 사용합니다.
        callback_url = f"http://{spring_boot_public_ip}:8080/api/tips/internal/tips/update-from-ai"

        payload = {
            "tipNo": tip_id,
            "title": result.get("title"),
            "contentSummary": result.get("summary"),
            "tags": result.get("tags", []),
            "thumbnailUrl": result.get("thumbnail_url")
        }
        
        print(f"콜백 요청 시작: URL={callback_url}, Payload={payload}")
        response = requests.post(callback_url, json=payload, timeout=15)
        response.raise_for_status()
        print(f"콜백 성공: tip_id {tip_id}, 상태 코드: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[에러] 콜백 요청 실패: tip_id {tip_id}")
        print(f" - 대상 URL: {e.request.url if e.request else 'N/A'}")
        print(f" - 오류 내용: {e}")
    
    return result
