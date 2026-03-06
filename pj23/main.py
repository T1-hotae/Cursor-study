# -*- coding: utf-8 -*-
"""
고객 리뷰 엑셀 데이터를 읽어 분석 후, ChatGPT API로 보고서를 생성합니다.
컬럼명 기반: 리뷰내용(고객리뷰), 평점(평점) + 그 외 컬럼 참고.
"""

import os
import sys
from datetime import datetime

from analyzer import analyze
from excel_loader import load_reviews_from_excel
from report_generator import generate_report


def main() -> None:
    print("고객 리뷰 데이터 분석 및 보고서 생성")
    print("-" * 50)

    # 1. 엑셀 로드 (컬럼명 기반)
    try:
        rows, headers, review_col, rating_col = load_reviews_from_excel()
    except FileNotFoundError as e:
        print(f"오류: {e}")
        sys.exit(1)

    print(f"엑셀 로드 완료: 데이터 {len(rows)}행, 컬럼 {headers}")
    if review_col:
        print(f"  - 고객 리뷰 컬럼: '{review_col}'")
    else:
        print("  - 경고: '리뷰내용'에 해당하는 컬럼을 찾지 못했습니다. 보고서에 리뷰 내용이 반영되지 않을 수 있습니다.")
    if rating_col:
        print(f"  - 평점 컬럼: '{rating_col}'")
    else:
        print("  - 경고: '평점'에 해당하는 컬럼을 찾지 못했습니다.")

    # 2. 분석에 쓸 기타 컬럼 (리뷰/평점 제외)
    other = [h for h in headers if h and h not in (review_col, rating_col)]

    # 3. 분석
    analysis = analyze(rows, review_col, rating_col, other_columns=other)
    print(f"분석 완료: 평균 평점 {analysis['avg_rating']}, 리뷰 수 {analysis['review_count']}")

    # 4. 보고서용 추가 컨텍스트 (컬럼 존재 여부 등)
    extra_context = {
        "사용된 컬럼": ", ".join(headers),
        "기타 참고 컬럼": ", ".join(other) if other else "없음",
    }

    # 5. OpenAI로 보고서 생성
    print("OpenAI API로 보고서 생성 중...")
    try:
        report_body = generate_report(analysis, extra_context)
    except ValueError as e:
        print(f"설정 오류: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"API 오류: {e}")
        sys.exit(1)

    # 6. 마크다운 보고서 저장
    title = "고객 리뷰 데이터 분석 보고서"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"# {title}\n\n생성 시각: {generated_at}\n\n데이터: {len(rows)}건, 리뷰 컬럼: {review_col or '-'}, 평점 컬럼: {rating_col or '-'}\n\n---\n\n{report_body}"

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "리뷰_분석_보고서.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"보고서 저장 완료: {out_path}")


if __name__ == "__main__":
    main()
