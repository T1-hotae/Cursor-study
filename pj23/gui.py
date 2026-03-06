# -*- coding: utf-8 -*-
"""
고객 리뷰 분석 보고서 생성기 - GUI
엑셀 파일을 첨부(선택)하면 보고서를 생성하고 마크다운(.md) 파일로 저장합니다.
"""

import os
import queue
import threading
from datetime import datetime
from tkinter import (
    Button,
    Entry,
    Frame,
    Label,
    StringVar,
    Tk,
    filedialog,
    messagebox,
    scrolledtext,
)

from analyzer import analyze
from excel_loader import load_reviews_from_excel
from report_generator import generate_report


def run_report_task(excel_path: str, status_queue: queue.Queue) -> None:
    """
    백그라운드에서: 엑셀 로드 → 분석 → API 보고서 생성 → 마크다운 저장.
    결과는 status_queue에 ("done", 경로) 또는 ("error", 메시지)로 전달.
    """
    try:
        status_queue.put("엑셀 파일 로드 중...")
        rows, headers, review_col, rating_col = load_reviews_from_excel(path=excel_path)
        status_queue.put(f"엑셀 로드 완료: {len(rows)}행, 리뷰 컬럼 '{review_col}', 평점 컬럼 '{rating_col}'")

        other = [h for h in headers if h and h not in (review_col, rating_col)]
        status_queue.put("데이터 분석 중...")
        analysis = analyze(rows, review_col, rating_col, other_columns=other)
        status_queue.put(f"분석 완료: 평균 평점 {analysis['avg_rating']}, 리뷰 {analysis['review_count']}건")

        extra_context = {
            "사용된 컬럼": ", ".join(headers),
            "기타 참고 컬럼": ", ".join(other) if other else "없음",
        }
        status_queue.put("OpenAI API로 보고서 생성 중... (잠시 기다려 주세요)")
        report_body = generate_report(analysis, extra_context)

        base_dir = os.path.dirname(os.path.abspath(excel_path))
        out_path = os.path.join(base_dir, "리뷰_분석_보고서.md")

        title = "고객 리뷰 데이터 분석 보고서"
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        report = (
            f"# {title}\n\n"
            f"생성 시각: {generated_at}\n\n"
            f"데이터: {len(rows)}건, 리뷰 컬럼: {review_col or '-'}, 평점 컬럼: {rating_col or '-'}\n\n"
            f"---\n\n{report_body}"
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        status_queue.put(("done", out_path))
    except Exception as e:
        status_queue.put(("error", str(e)))


def main() -> None:
    root = Tk()
    root.title("고객 리뷰 분석 보고서 생성기")
    root.geometry("620x360")
    root.resizable(True, True)

    excel_path_var = StringVar()
    status_queue = queue.Queue()

    # 엑셀 파일 선택
    top = Frame(root, padx=12, pady=10)
    top.pack(fill="x")

    Label(top, text="엑셀 파일:", width=10, anchor="w").pack(side="left", padx=(0, 6))
    entry = Entry(top, textvariable=excel_path_var, state="readonly", width=50)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

    def browse() -> None:
        path = filedialog.askopenfilename(
            title="리뷰 데이터 엑셀 선택",
            filetypes=[("Excel 파일", "*.xlsx"), ("모든 파일", "*.*")],
        )
        if path:
            excel_path_var.set(path)

    btn_browse = Button(top, text="찾아보기", command=browse)
    btn_browse.pack(side="left")

    # 진행 상황 로그
    log_frame = Frame(root, padx=12, pady=8)
    log_frame.pack(fill="both", expand=True)
    Label(log_frame, text="진행 상황:", anchor="w").pack(fill="x")
    status_text = scrolledtext.ScrolledText(log_frame, height=10, wrap="word", font=("Consolas", 9))
    status_text.pack(fill="both", expand=True)
    status_text.tag_configure("success", foreground="green")
    status_text.tag_configure("error", foreground="red")

    # 보고서 생성 버튼
    def poll_queue() -> None:
        try:
            while True:
                msg = status_queue.get_nowait()
                if isinstance(msg, tuple):
                    kind, val = msg
                    if kind == "done":
                        status_text.insert("end", f"저장 완료: {val}\n", "success")
                        btn_generate.config(state="normal")
                        btn_browse.config(state="normal")
                        messagebox.showinfo("완료", f"보고서가 저장되었습니다.\n\n{val}")
                    else:
                        status_text.insert("end", f"오류: {val}\n", "error")
                        btn_generate.config(state="normal")
                        btn_browse.config(state="normal")
                        messagebox.showerror("오류", val)
                    return
                status_text.insert("end", msg + "\n")
                status_text.see("end")
        except queue.Empty:
            pass
        root.after(200, poll_queue)

    def start_generate() -> None:
        path = excel_path_var.get().strip()
        if not path:
            messagebox.showwarning("파일 선택", "엑셀 파일을 선택해 주세요.")
            return
        if not path.lower().endswith(".xlsx"):
            messagebox.showwarning("파일 형식", ".xlsx 파일을 선택해 주세요.")
            return

        status_text.delete("1.0", "end")
        status_text.insert("end", "보고서 생성 시작...\n")
        btn_generate.config(state="disabled")
        btn_browse.config(state="disabled")
        threading.Thread(target=lambda: run_report_task(path, status_queue), daemon=True).start()
        poll_queue()

    mid = Frame(root, padx=12, pady=6)
    mid.pack(fill="x")
    btn_generate = Button(mid, text="보고서 생성 (마크다운 저장)", command=start_generate, width=28)
    btn_generate.pack(side="left")

    Label(
        root,
        text="보고서는 선택한 엑셀 파일과 같은 폴더에 '리뷰_분석_보고서.md'로 저장됩니다.",
        font=("", 9),
        fg="gray",
    ).pack(anchor="w", padx=12, pady=0)

    root.mainloop()


if __name__ == "__main__":
    main()
