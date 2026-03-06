"""
PDF 내용을 OpenAI GPT(gpt-4o-mini)로 요약하여 저장하는 프로그램.

API 키는 반드시 환경 변수 OPENAI_API_KEY로 설정하세요.
  PowerShell: $env:OPENAI_API_KEY="your-api-key"
  CMD: set OPENAI_API_KEY=your-api-key
"""

import os
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("pdfplumber가 필요합니다. pip install pdfplumber")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("openai 패키지가 필요합니다. pip install openai")
    sys.exit(1)


# 토큰 수 대략 제한 (gpt-4o-mini 컨텍스트 128k, 여유 있게 100k 문자까지 한 번에 요약)
MAX_CHARS_PER_REQUEST = 100_000


def extract_text_from_pdf(pdf_path: str) -> str:
    """단일 PDF 파일에서 텍스트를 추출합니다."""
    text_parts = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        return "\n".join(text_parts)
    except Exception as e:
        return f"[오류: {e}]"


def get_pdf_files(folder: Path) -> list[Path]:
    """폴더 내 모든 PDF 파일 경로를 반환합니다."""
    return sorted(folder.glob("*.pdf"))


def summarize_with_gpt(client: OpenAI, text: str, model: str = "gpt-4o-mini") -> str:
    """GPT로 텍스트를 요약합니다. 텍스트가 길면 앞부분만 잘라 요약합니다."""
    if not text or not text.strip():
        return "(추출된 텍스트가 없어 요약할 수 없습니다.)"

    # 너무 길면 잘라서 요약 (컨텍스트 여유 확보)
    if len(text) > MAX_CHARS_PER_REQUEST:
        text = text[:MAX_CHARS_PER_REQUEST] + "\n\n[... 이하 생략 ...]"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "당신은 문서 요약 전문가입니다. 주어진 텍스트를 한국어로 핵심만 간결하게 요약해 주세요. "
                "제목, 주요 내용, 결론/요점 순으로 정리해 주세요.",
            },
            {"role": "user", "content": f"다음 텍스트를 요약해 주세요:\n\n{text}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or "(요약 생성 실패)"


def main():
    script_dir = Path(__file__).parent.resolve()
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        print("오류: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("  PowerShell: $env:OPENAI_API_KEY=\"your-api-key\"")
        print("  CMD: set OPENAI_API_KEY=your-api-key")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    pdf_files = get_pdf_files(script_dir)

    if not pdf_files:
        print("현재 폴더에 PDF 파일이 없습니다.")
        return

    output_dir = script_dir / "summaries"
    output_dir.mkdir(exist_ok=True)

    model = "gpt-4o-mini"
    print(f"모델: {model}")
    print(f"총 {len(pdf_files)}개 PDF 요약 중...\n")

    for pdf_path in pdf_files:
        print(f"  처리 중: {pdf_path.name}")
        text = extract_text_from_pdf(str(pdf_path))
        if text.startswith("[오류:"):
            summary = text
        else:
            try:
                summary = summarize_with_gpt(client, text, model=model)
            except Exception as e:
                summary = f"[API 오류: {e}]"

        out_name = pdf_path.stem + "_summary.txt"
        out_path = output_dir / out_name
        out_path.write_text(summary, encoding="utf-8")
        print(f"    저장됨: {out_path}")

    print(f"\n요약이 '{output_dir}' 폴더에 저장되었습니다.")


if __name__ == "__main__":
    main()
