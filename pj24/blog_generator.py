"""
키워드와 참고 자료(텍스트 파일)를 입력받아 GPT API로 창의적인 블로그 글을 생성하는 프로그램.
가성비를 위해 gpt-4o-mini 모델을 사용합니다.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 로드 (프로젝트 루트 기준)
load_dotenv(Path(__file__).resolve().parent / ".env")

# gpt-4o-mini: 입력/출력 단가가 낮고 창의적 글쓰기에 충분한 성능 (가성비 우수)
MODEL_NAME = "gpt-4o-mini"


def get_client() -> OpenAI | None:
    """환경 변수에서 API 키를 읽어 OpenAI 클라이언트를 반환합니다. 실패 시 None."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your-"):
        print("오류: .env 파일에 OPENAI_API_KEY를 설정해 주세요.", file=sys.stderr)
        print("  .env.example을 참고해 .env 파일을 만들고 키를 입력하세요.", file=sys.stderr)
        return None
    return OpenAI(api_key=api_key)


def read_reference_file(file_path: str) -> str:
    """텍스트 파일 내용을 UTF-8로 읽어 반환합니다. 파일이 없거나 읽기 실패 시 빈 문자열."""
    path = Path(file_path)
    if not path.exists():
        print(f"경고: 참고 자료 파일을 찾을 수 없습니다. ({file_path})")
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"경고: 참고 자료 파일을 읽는 중 오류가 발생했습니다. ({e})")
        return ""


# 글 스타일: 친근하게 / 진지하게
STYLE_FRIENDLY = "friendly"
STYLE_SERIOUS = "serious"
STYLE_CHOICES = (STYLE_FRIENDLY, STYLE_SERIOUS)


def generate_blog_post(
    client: OpenAI,
    keyword: str,
    reference_text: str = "",
    perspective: str = "",
    style: str = STYLE_FRIENDLY,
) -> str:
    """키워드, 참고 자료, 나의 관점, 스타일을 바탕으로 창의적인 블로그 글을 생성합니다."""
    style_instruction = (
        "글의 톤은 **친근하게** 써 주세요. 반말은 쓰지 않고, 구어체·경어를 섞어 편하게 읽히도록 하세요."
        if style == STYLE_FRIENDLY
        else "글의 톤은 **진지하게** 써 주세요. 격식 있는 문어체로, 신뢰감 있는 논조를 유지하세요."
    )
    system_prompt = f"""당신은 독자의 관심을 끌고 가치 있는 인사이트를 전달하는 블로그 작가입니다.
주어진 키워드를 주제로, 참고 자료(있다면)와 작성자의 관점(있다면)을 반영해 독창적이고 읽기 쉬운 블로그 글을 작성해 주세요.
- 서론, 본문 2~3개 섹션, 마무리로 구성해 주세요.
- {style_instruction}
- 작성자의 관점이 있으면 그 시각과 톤을 살리면서 글을 풀어내 주세요.
- 참고 자료가 있으면 그 내용을 바탕으로 설득력 있게 쓰고, 없으면 키워드만으로 창의적으로 풀어내 주세요.
- 과장 없이 쓰고, 필요하면 구체적인 예시를 들어 주세요.
- 글은 한국어로 작성하고, 블로그에 바로 붙여넣기 할 수 있는 형태로 출력해 주세요."""

    user_parts = [f"다음 키워드로 창의적인 블로그 글을 써 주세요.\n\n키워드: {keyword}"]
    if perspective.strip():
        user_parts.append(
            "\n\n--- 작성자(나)의 관점입니다. 이 시각을 반영해 블로그 글을 작성해 주세요. ---\n\n"
            + perspective.strip()
        )
    if reference_text:
        user_parts.append(
            "\n\n--- 아래는 참고 자료입니다. 이 내용을 반영해 블로그 글을 작성해 주세요. ---\n\n"
            + reference_text
        )
    user_prompt = "\n".join(user_parts)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,  # 창의성 확보
        max_tokens=2000,
    )
    return response.choices[0].message.content or ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="키워드와 참고 자료(텍스트 파일)로 블로그 글을 생성합니다."
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        default=None,
        help="블로그 글의 주제 키워드 (미입력 시 실행 후 입력)",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="ref_file",
        metavar="파일경로",
        default=None,
        help="참고 자료가 담긴 텍스트 파일 경로 (선택)",
    )
    parser.add_argument(
        "-p",
        "--perspective",
        dest="perspective",
        metavar="관점",
        default=None,
        help="나의 관점 200자 내외 (선택)",
    )
    parser.add_argument(
        "-s",
        "--style",
        dest="style",
        choices=["friendly", "serious"],
        default=None,
        help="글 스타일: friendly(친근하게), serious(진지하게)",
    )
    args = parser.parse_args()

    keyword = args.keyword
    if not keyword:
        keyword = input("블로그 글의 키워드를 입력하세요: ").strip()

    if not keyword:
        print("키워드를 입력해 주세요.")
        sys.exit(1)

    perspective = args.perspective
    if perspective is None:
        perspective = input(
            "나의 관점을 200자 내외로 입력 (없으면 Enter): "
        ).strip()

    style = args.style
    if style is None:
        style_in = input(
            "글 스타일 (1: 친근하게, 2: 진지하게, Enter=친근하게): "
        ).strip() or "1"
        style = STYLE_FRIENDLY if style_in == "1" else STYLE_SERIOUS

    ref_file = args.ref_file
    if not ref_file:
        ref_file = input(
            "참고 자료 텍스트 파일 경로 (없으면 Enter): "
        ).strip()

    reference_text = read_reference_file(ref_file) if ref_file else ""

    if reference_text or perspective:
        parts = [f"키워드 '{keyword}'"]
        if perspective:
            parts.append(f"나의 관점({len(perspective)}자)")
        if reference_text:
            parts.append(f"참고 자료({len(reference_text)}자)")
        print(f"\n{', '.join(parts)}로 블로그 글을 생성 중입니다... (모델: {MODEL_NAME})\n")
    else:
        print(f"\n키워드 '{keyword}'로 블로그 글을 생성 중입니다... (모델: {MODEL_NAME})\n")

    client = get_client()
    if client is None:
        sys.exit(1)
    content = generate_blog_post(
        client, keyword, reference_text, perspective, style
    )
    print(content)


if __name__ == "__main__":
    main()
