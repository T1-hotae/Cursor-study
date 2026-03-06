# -*- coding: utf-8 -*-
"""설정: 주요 컬럼명 및 API 옵션"""

# 엑셀 주요 컬럼 (컬럼명 기반 접근)
COLUMN_REVIEW = "리뷰내용"   # 고객 리뷰
COLUMN_RATING = "평점"       # 평점

# 리뷰/평점 컬럼 후보 (다른 이름으로 올 수 있는 경우)
REVIEW_COLUMN_CANDIDATES = ["리뷰내용", "리뷰", "내용", "Review", "review_content"]
RATING_COLUMN_CANDIDATES = ["평점", "별점", "Rating", "rating", "점수"]

# 보고서 생성용 OpenAI 모델 (보고서 품질에 적합)
REPORT_MODEL = "gpt-4o-mini"  # 비용·품질 균형. 더 높은 품질 원하면 gpt-4o 로 변경
