"""
현재 폴더의 PDF 파일들에서 텍스트를 추출하는 프로그램 (pdfplumber 사용)
"""

import os
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("pdfplumber가 설치되어 있지 않습니다. 'pip install pdfplumber' 로 설치해주세요.")
    exit(1)


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


def get_pdf_files(folder: str = ".") -> list[str]:
    """폴더 내 모든 PDF 파일 경로를 반환합니다."""
    folder_path = Path(folder).resolve()
    return sorted(folder_path.glob("*.pdf"))


def save_all_to_txt(pdf_files: list, output_dir: Path) -> None:
    """모든 PDF의 텍스트를 output_dir에 .txt로 저장합니다."""
    output_dir.mkdir(exist_ok=True)
    for pdf_path in pdf_files:
        text = extract_text_from_pdf(str(pdf_path))
        out_name = pdf_path.stem + "_extracted.txt"
        out_path = output_dir / out_name
        out_path.write_text(text, encoding="utf-8")
        print(f"  저장됨: {out_path}")
    print(f"\n모든 텍스트가 '{output_dir}' 폴더에 저장되었습니다.")


def main():
    import sys

    # 현재 스크립트가 있는 폴더 기준
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    # --save 옵션: 텍스트를 파일로 저장 (대화형 프롬프트 없음)
    auto_save = "--save" in sys.argv or "-s" in sys.argv

    pdf_files = get_pdf_files(script_dir)

    if not pdf_files:
        print("현재 폴더에 PDF 파일이 없습니다.")
        return

    print(f"총 {len(pdf_files)}개의 PDF 파일을 찾았습니다.\n")
    print("=" * 60)

    for pdf_path in pdf_files:
        print(f"\n📄 {pdf_path.name}")
        print("-" * 60)
        text = extract_text_from_pdf(str(pdf_path))
        if text.strip():
            # 미리보기: 처음 500자만 출력
            preview = text.strip()[:500]
            if len(text.strip()) > 500:
                preview += "\n... (이하 생략)"
            print(preview)
        else:
            print("(추출된 텍스트 없음 - 스캔된 이미지 PDF일 수 있음)")
        print()

    if auto_save:
        output_dir = script_dir / "extracted_text"
        save_all_to_txt(pdf_files, output_dir)
    else:
        # 각 PDF별로 텍스트 파일로 저장할지 묻기
        try:
            save = input("각 PDF의 전체 텍스트를 .txt 파일로 저장할까요? (y/n): ").strip().lower()
        except EOFError:
            save = "n"
        if save == "y":
            output_dir = script_dir / "extracted_text"
            save_all_to_txt(pdf_files, output_dir)


if __name__ == "__main__":
    main()
