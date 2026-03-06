# -*- coding: utf-8 -*-
"""OpenAI API로 분석 결과를 바탕으로 상급자 보고용 보고서 생성 (표·목록 중심)"""

import os
from typing import Any, Optional

from dotenv import load_dotenv
from openai import OpenAI

from config import REPORT_MODEL

load_dotenv()


def _format_rating_table(dist: dict) -> str:
    """평점 분포를 표 형태 문자열로."""
    total = sum(dist.values())
    lines = ["| 평점 | 건수 | 비율(%) |", "|------|------|--------|"]
    for k in [1, 2, 3, 4, 5]:
        cnt = dist.get(k, 0)
        pct = round(100 * cnt / total, 1) if total else 0
        lines.append(f"| {k}점 | {cnt}건 | {pct}% |")
    lines.append(f"| **합계** | **{total}건** | 100% |")
    return "\n".join(lines)


def _format_product_table(products: list[dict]) -> str:
    """제품별 요약을 표 형태로."""
    if not products:
        return "(제품별 데이터 없음)"
    lines = ["| 제품명 | 리뷰 수 | 평균 평점 |", "|--------|--------|----------|"]
    for p in products[:25]:
        lines.append(f"| {p.get('제품명', '-')} | {p.get('리뷰 수', 0)}건 | {p.get('평균 평점', '-')} |")
    return "\n".join(lines)


def _format_satisfaction_table(sat: Optional[dict]) -> str:
    if not sat:
        return "(만족도 데이터 없음)"
    total = sum(sat.values())
    lines = ["| 구분 | 건수 | 비율(%) |", "|------|------|--------|"]
    for k, v in sat.items():
        pct = round(100 * v / total, 1) if total else 0
        lines.append(f"| {k} | {v}건 | {pct}% |")
    lines.append(f"| **합계** | **{total}건** | 100% |")
    return "\n".join(lines)


def _format_usage_table(usage: Optional[dict]) -> str:
    if not usage:
        return "(사용기간 데이터 없음)"
    total = sum(usage.values())
    lines = ["| 사용기간 | 건수 | 비율(%) |", "|----------|------|--------|"]
    for k, v in sorted(usage.items(), key=lambda x: -x[1]):
        pct = round(100 * v / total, 1) if total else 0
        lines.append(f"| {k} | {v}건 | {pct}% |")
    return "\n".join(lines)


def build_prompt(analysis: dict, extra_context: dict[str, Any]) -> str:
    """상급자 보고용 보고서 지시와 데이터를 담은 프롬프트를 만듭니다."""
    dist = analysis.get("rating_distribution") or {}
    rating_table = _format_rating_table(dist)
    product_table = _format_product_table(analysis.get("product_summary") or [])
    sat_table = _format_satisfaction_table(analysis.get("satisfaction"))
    usage_table = _format_usage_table(analysis.get("usage_period_summary"))
    date_range = analysis.get("date_range")
    date_str = f"{date_range[0]} ~ {date_range[1]}" if date_range and date_range[0] else "(없음)"

    samples = analysis.get("sample_reviews") or []
    sample_lines = []
    for i, s in enumerate(samples[:18], 1):
        parts = [f"{k}: {v}" for k, v in (s if isinstance(s, dict) else {}).items()]
        sample_lines.append(f"{i}. " + " | ".join(parts))

    system = """당신은 경영진·상급자에게 보고하는 고객 리뷰 분석 보고서 전문가입니다.
다음 규칙을 반드시 지킵니다.
1. **표(markdown table)**를 적극 사용: 주요 지표, 평점 분포, 제품별 현황, 만족도·사용기간 등 숫자 데이터는 반드시 표로 제시합니다.
2. **목록**을 사용: 핵심 발견 사항은 번호 목록(1. 2. 3.) 또는 불릿(-)으로 정리합니다. 줄글만 나열하지 않습니다.
3. **구성**: 경영진 요약 → 데이터 현황(표) → 평점 분석(표+해석) → 제품별/만족도/사용기간(표) → 리뷰 내용 분석(목록·키워드) → 시사점 및 제안(번호 목록).
4. **분량**: 상급자 보고용으로 충분한 분량(표·목록 포함해 A4 2~3페이지 분량)으로 작성합니다. 짧은 요약 수준이 아닌, 일목요연한 보고서 형태로 작성합니다.
5. **문체**: 격식 있는 보고 문체, 한국어, 마크다운(##, ###, 표, 목록)을 사용합니다."""

    user_parts = [
        "아래 데이터를 바탕으로 **상급자 보고용** 고객 리뷰 분석 보고서를 작성해 주세요.",
        "제공된 표 형식 데이터는 보고서 안에 **그대로 또는 정리한 표**로 반드시 포함하고, 추가 해석과 리뷰 내용 요약(긍정/부정 키워드, 트렌드)을 보강해 주세요.",
        "",
        "## 제공 데이터 (보고서에 표·목록으로 반영할 것)",
        "",
        "### 주요 지표",
        f"- 총 데이터 수: {analysis.get('total_count', 0)}건",
        f"- 리뷰 내용 있음: {analysis.get('review_count', 0)}건",
        f"- 평균 평점: {analysis.get('avg_rating', '-')}",
        f"- 조사 기간(구매일자 기준): {date_str}",
        "",
        "### 평점 분포 (아래를 보고서에 표로 포함)",
        rating_table,
        "",
        "### 제품별 리뷰·평균 평점 (보고서에 표로 포함)",
        product_table,
        "",
        "### 만족도 현황 (보고서에 표로 포함)",
        sat_table,
        "",
        "### 사용기간별 현황 (보고서에 표로 포함)",
        usage_table,
        "",
        "### 샘플 리뷰 (일부, 리뷰 내용 요약·키워드 추출에 활용)",
        "\n".join(sample_lines),
        "",
    ]
    if extra_context:
        user_parts.append("### 참고 컨텍스트")
        for k, v in extra_context.items():
            user_parts.append(f"- {k}: {v}")
        user_parts.append("")

    user_parts.extend([
        "---",
        "위 데이터만 사용하여, **표와 목록을 반드시 포함한** 상급자 보고용 보고서 본문을 작성해 주세요. 제목(# 고객 리뷰 데이터 분석 보고서)은 제외하고, 본문부터 작성합니다.",
    ])

    return system, "\n".join(user_parts)


def generate_report(analysis: dict, extra_context: Optional[dict[str, Any]] = None) -> str:
    """OpenAI API를 호출해 보고서 본문을 생성합니다."""
    if extra_context is None:
        extra_context = {}
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY=your_key 형태로 넣어 주세요."
        )
    client = OpenAI(api_key=api_key)
    system, user_content = build_prompt(analysis, extra_context)
    response = client.chat.completions.create(
        model=REPORT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
