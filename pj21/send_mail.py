# -*- coding: utf-8 -*-
"""
축산메일실습용.xlsx 고객에게 Gmail SMTP로 메일 발송 (테스트: 발신/수신 동일, 10건만)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import openpyxl
import os

# 테스트 설정
TEST_SENDER = "ghxo03215@gmail.com"
TEST_RECEIVER = "ghxo03215@gmail.com"
MAX_SEND_COUNT = 10
EXCEL_FILE = "축산메일실습용.xlsx"


def load_customers(excel_path: str, max_rows: int = 10) -> List[Dict]:
    """엑셀에서 상위 max_rows개 행을 읽어 리스트[딕셔너리]로 반환."""
    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if not rows:
        return []
    headers = [str(h).strip() if h is not None else f"Col{i}" for i, h in enumerate(rows[0])]
    data = []
    for row in rows[1 : max_rows + 1]:
        if row is None:
            continue
        data.append(dict(zip(headers, (v if v is not None else "" for v in row))))
    return data


def send_gmail_smtp(
    sender: str,
    receiver: str,
    password: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
) -> None:
    """Gmail SMTP로 메일 1통 발송."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())


def main():
    excel_path = os.path.join(os.path.dirname(__file__), EXCEL_FILE)
    if not os.path.isfile(excel_path):
        print(f"엑셀 파일을 찾을 수 없습니다: {excel_path}")
        return

    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        print("Gmail 앱 비밀번호가 필요합니다.")
        print("  방법: Gmail → Google 계정 → 보안 → 2단계 인증 켜기 → 앱 비밀번호 생성")
        print("  터미널에서 설정: set GMAIL_APP_PASSWORD=생성한16자리비밀번호")
        pwd = input("앱 비밀번호를 입력하세요 (또는 Enter로 종료): ").strip()
        if not pwd:
            return
        password = pwd

    customers = load_customers(excel_path, max_rows=MAX_SEND_COUNT)
    if not customers:
        print("엑셀에서 읽을 데이터가 없습니다.")
        return

    print(f"엑셀에서 {len(customers)}건 로드. 테스트 모드: 수신자 모두 {TEST_RECEIVER}")
    for i, row in enumerate(customers, 1):
        # 엑셀에 '이름' 또는 '고객명' 등이 있으면 제목/본문에 사용
        name = (row.get("이름") or row.get("고객명") or row.get("성명") or "").strip() or f"고객{i}"
        subject = f"[축산 메일 테스트] {name}님께"
        body_text = f"{name}님 안녕하세요.\n\n축산 관련 메일 테스트입니다.\n\n(본 메일은 테스트로 발신/수신이 동일 주소입니다.)"
        body_html = f"<p>{name}님 안녕하세요.</p><p>축산 관련 메일 테스트입니다.</p><p><small>(테스트 발송)</small></p>"
        try:
            send_gmail_smtp(
                sender=TEST_SENDER,
                receiver=TEST_RECEIVER,
                password=password,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
            )
            print(f"  {i}/{len(customers)} 발송 완료: {subject}")
        except Exception as e:
            print(f"  {i}/{len(customers)} 발송 실패: {e}")
    print("완료.")


if __name__ == "__main__":
    main()
