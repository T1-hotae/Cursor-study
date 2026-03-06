# -*- coding: utf-8 -*-
"""컬럼명 기반 엑셀 로더"""

import glob
import os
from typing import Any, Optional

import openpyxl

from config import (
    COLUMN_RATING,
    COLUMN_REVIEW,
    RATING_COLUMN_CANDIDATES,
    REVIEW_COLUMN_CANDIDATES,
)


def _normalize(s: Any) -> str:
    if s is None:
        return ""
    return str(s).strip()


def _find_column_index(header_row: list, candidates: list) -> Optional[int]:
    """헤더 행에서 후보 이름 중 처음 매칭되는 열 인덱스 반환 (0-based)."""
    for i, cell in enumerate(header_row):
        val = _normalize(cell)
        for cand in candidates:
            if val == cand or val.lower() == cand.lower():
                return i
    return None


def load_reviews_from_excel(
    path: Optional[str] = None,
    sheet_name: Optional[str] = None,
) -> tuple[list[dict], list[str], Optional[str], Optional[str]]:
    """
    엑셀 파일을 읽어 리뷰 데이터를 반환합니다.
    - path: 파일 경로. None이면 현재 폴더에서 첫 .xlsx 사용.
    - sheet_name: 시트 이름. None이면 활성 시트.

    Returns:
        (rows, headers, review_col_idx, rating_col_idx)
        rows: 각 행이 dict (헤더명 -> 셀 값)
        headers: 헤더 이름 리스트
        review_col_name, rating_col_name: 리뷰/평점 열 이름 (찾지 못하면 None)
    """
    if path is None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        files = glob.glob("*.xlsx")
        if not files:
            raise FileNotFoundError("현재 폴더에 .xlsx 파일이 없습니다.")
        path = files[0]

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active
    rows_iter = list(ws.iter_rows(values_only=True))
    wb.close()

    if not rows_iter:
        return [], [], None, None

    header_row = [(_normalize(c) or f"Column_{i}") for i, c in enumerate(rows_iter[0])]
    review_col_idx = _find_column_index(header_row, REVIEW_COLUMN_CANDIDATES)
    rating_col_idx = _find_column_index(header_row, RATING_COLUMN_CANDIDATES)

    # 기본 컬럼명이 있으면 해당 이름으로도 사용 (리포트에서 참조)
    if review_col_idx is None and COLUMN_REVIEW in header_row:
        review_col_idx = header_row.index(COLUMN_REVIEW)
    if rating_col_idx is None and COLUMN_RATING in header_row:
        rating_col_idx = header_row.index(COLUMN_RATING)

    rows = []
    for r in rows_iter[1:]:
        row = {}
        for i, h in enumerate(header_row):
            if i < len(r):
                val = r[i]
                if hasattr(val, "isoformat"):  # datetime
                    val = val.isoformat()[:10] if val else ""
                row[h] = val
        rows.append(row)

    review_col_name = header_row[review_col_idx] if review_col_idx is not None else None
    rating_col_name = header_row[rating_col_idx] if rating_col_idx is not None else None
    return rows, header_row, review_col_name, rating_col_name
