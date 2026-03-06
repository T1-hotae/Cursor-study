# -*- coding: utf-8 -*-
"""리뷰 데이터 분석 (평점·리뷰·제품별·만족도 등)"""

from collections import Counter, defaultdict
from typing import Any, Optional

import re


def _safe_float(v: Any) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    return str(v).strip()


def _is_date_like(v: Any) -> bool:
    if v is None or v == "":
        return False
    s = str(v)
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}", s)) or bool(re.match(r"^\d{4}/\d{2}/\d{2}", s))


def analyze(
    rows: list[dict],
    review_col: Optional[str],
    rating_col: Optional[str],
    other_columns: Optional[list[str]] = None,
) -> dict:
    """
    리뷰 행 목록을 분석해 통계·제품별·만족도·기간 등 집계를 반환합니다.
    """
    if other_columns is None:
        other_columns = []

    total = len(rows)
    ratings: list[float] = []
    reviews: list[str] = []
    samples: list[dict] = []

    # 제품별 집계 (노트북명, 제품명 등)
    by_product: dict[str, list[float]] = defaultdict(list)
    # 만족도 집계
    satisfaction: dict[str, int] = defaultdict(int)
    # 사용기간 집계
    by_usage: dict[str, int] = defaultdict(int)
    date_values: list[str] = []

    for row in rows:
        r_val = _safe_float(row.get(rating_col)) if rating_col else None
        if r_val is not None:
            ratings.append(r_val)
        rev = _safe_str(row.get(review_col)) if review_col else ""
        reviews.append(rev)
        sample = {}
        if review_col:
            sample["리뷰"] = rev[:200] + ("..." if len(rev) > 200 else "")
        if rating_col and r_val is not None:
            sample["평점"] = r_val
        for col in other_columns:
            if col and col in row and col != review_col and col != rating_col:
                sample[col] = row[col]
                val = row[col]
                sval = _safe_str(val)
                if col in ("노트북명", "제품명", "상품명", "제품") and sval and r_val is not None:
                    by_product[sval].append(r_val)
                if col in ("만족도", "만족") and sval:
                    satisfaction[sval] += 1
                if col in ("사용기간", "사용 기간") and sval:
                    by_usage[sval] += 1
                if _is_date_like(val):
                    date_values.append(str(val)[:10])
        if sample:
            samples.append(sample)

    avg_rating = sum(ratings) / len(ratings) if ratings else None
    rating_dist = Counter(ratings) if ratings else Counter()
    distribution = {int(k): rating_dist.get(k, 0) + rating_dist.get(float(k), 0) for k in [1, 2, 3, 4, 5]}

    # 제품별 평균·건수
    product_summary: list[dict[str, Any]] = []
    for name, r_list in sorted(by_product.items(), key=lambda x: -len(x[1])):
        product_summary.append({
            "제품명": name,
            "리뷰 수": len(r_list),
            "평균 평점": round(sum(r_list) / len(r_list), 2),
        })

    return {
        "total_count": total,
        "review_count": len([r for r in reviews if r]),
        "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
        "rating_distribution": distribution,
        "sample_reviews": samples[:20],
        "all_review_texts": reviews,
        "product_summary": product_summary[:30],
        "satisfaction": dict(satisfaction) if satisfaction else None,
        "usage_period_summary": dict(by_usage) if by_usage else None,
        "date_range": (min(date_values), max(date_values)) if date_values else None,
    }
