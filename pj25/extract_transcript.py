"""
YouTube 영상 자막 추출 + 한글 맞춤법 검사
- youtube-transcript-api (1.1.1 이상) 사용
- Webshare 프록시를 통한 요청 (IP 차단 우회)
- 자막을 한 덩이 텍스트로 합친 뒤 GPT로 맞춤법 검사
"""

import os

from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

load_dotenv()

# 맞춤법 검사용 프롬프트
SPELL_CHECK_SYSTEM = """당신은 한국어 맞춤법과 문법을 정확히 고치는 전문가입니다.
주어진 텍스트에서 다음을 수정해 주세요:
- 맞춤법 오류 (띄어쓰기, 맞춤법 규정)
- 문법 오류 및 어색한 표현
- 띄어쓰기 통일

원문의 의미와 말투는 유지하면서, 수정된 전체 텍스트만 출력하세요. 설명이나 주석은 붙이지 마세요."""


def fetch_transcript_as_one_block(video_id: str) -> str:
    """한글 자막을 우선으로 가져와 한 덩이 텍스트로 반환."""
    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username="lgbnqldp",
            proxy_password="160wcu70eb5r",
        )
    )
    transcript = ytt_api.fetch(video_id, languages=["ko", "en-US"])
    # 한 덩이로: 스니펫 텍스트를 공백으로 이어붙임
    return " ".join(snippet.text for snippet in transcript)


def spell_check_with_gpt(text: str, api_key: str) -> str:
    """GPT로 맞춤법 검사 후 수정된 텍스트 반환."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SPELL_CHECK_SYSTEM},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()


def main():
    video_id = "e9fC9bUdxsE"

    print("자막 추출 중...")
    raw_text = fetch_transcript_as_one_block(video_id)

    print("=" * 60)
    print("[ 원본 자막 (한 덩이) ]")
    print("=" * 60)
    print(raw_text)
    print()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return

    print("맞춤법 검사 중 (GPT)...")
    corrected = spell_check_with_gpt(raw_text, api_key)

    print("=" * 60)
    print("[ 맞춤법 검사 결과 ]")
    print("=" * 60)
    print(corrected)
    print()
    print("완료.")


if __name__ == "__main__":
    main()
