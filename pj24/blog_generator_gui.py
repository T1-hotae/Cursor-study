"""
블로그 글 생성기 GUI.
키워드 입력과 참고 자료 파일 첨부 후 GPT API로 블로그 글을 생성합니다.
"""

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

# .env 로드 (blog_generator와 동일)
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from blog_generator import (
    MODEL_NAME,
    STYLE_FRIENDLY,
    STYLE_SERIOUS,
    generate_blog_post,
    get_client,
    read_reference_file,
)


def run_app() -> None:
    root = tk.Tk()
    root.title("블로그 글 생성기")
    root.geometry("720x560")
    root.minsize(520, 400)

    # 선택된 참고 파일 경로 (None = 미선택)
    selected_file_path: tk.StringVar = tk.StringVar(value="")

    # ---- 상단: 키워드 ----
    frame_top = tk.Frame(root, padx=12, pady=10)
    frame_top.pack(fill=tk.X)

    tk.Label(frame_top, text="키워드:", font=("", 10)).pack(side=tk.LEFT, padx=(0, 6))
    entry_keyword = tk.Entry(frame_top, font=("", 11), width=40)
    entry_keyword.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

    # ---- 참고 자료 파일 첨부 ----
    frame_file = tk.Frame(root, padx=12, pady=6)
    frame_file.pack(fill=tk.X)

    def choose_file() -> None:
        path = filedialog.askopenfilename(
            title="참고 자료 텍스트 파일 선택",
            filetypes=[
                ("텍스트 파일", "*.txt"),
                ("모든 파일", "*.*"),
            ],
        )
        if path:
            selected_file_path.set(path)

    tk.Button(frame_file, text="파일 첨부", command=choose_file, width=10).pack(
        side=tk.LEFT, padx=(0, 8)
    )
    label_file = tk.Label(
        frame_file,
        text="선택된 파일 없음",
        fg="gray",
        font=("", 9),
        anchor="w",
    )
    label_file.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_file_label(*args: object) -> None:
        path = selected_file_path.get()
        if path:
            name = Path(path).name
            label_file.config(text=name, fg="black")
        else:
            label_file.config(text="선택된 파일 없음", fg="gray")

    selected_file_path.trace_add("write", update_file_label)

    # ---- 나의 관점 (200자 내외) ----
    frame_perspective = tk.Frame(root, padx=12, pady=8)
    frame_perspective.pack(fill=tk.X)
    tk.Label(
        frame_perspective,
        text="나의 관점 (200자 내외, 선택):",
        font=("", 10),
    ).pack(anchor=tk.W)
    text_perspective = tk.Text(
        frame_perspective,
        height=3,
        font=("맑은 고딕", 10),
        wrap=tk.WORD,
        padx=6,
        pady=6,
    )
    text_perspective.pack(fill=tk.X, pady=(4, 0))

    # ---- 글 스타일 (친근하게 / 진지하게) ----
    style_var: tk.StringVar = tk.StringVar(value=STYLE_FRIENDLY)
    frame_style = tk.Frame(root, padx=12, pady=8)
    frame_style.pack(fill=tk.X)
    tk.Label(frame_style, text="글 스타일:", font=("", 10)).pack(
        side=tk.LEFT, padx=(0, 8)
    )
    tk.Radiobutton(
        frame_style,
        text="친근하게",
        variable=style_var,
        value=STYLE_FRIENDLY,
        font=("", 10),
        cursor="hand2",
    ).pack(side=tk.LEFT, padx=(0, 12))
    tk.Radiobutton(
        frame_style,
        text="진지하게",
        variable=style_var,
        value=STYLE_SERIOUS,
        font=("", 10),
        cursor="hand2",
    ).pack(side=tk.LEFT)

    # ---- 생성 버튼 ----
    frame_btn = tk.Frame(root, padx=12, pady=8)
    frame_btn.pack(fill=tk.X)

    output_text = scrolledtext.ScrolledText(
        root,
        font=("맑은 고딕", 10),
        wrap=tk.WORD,
        padx=10,
        pady=10,
    )
    output_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
    output_text.tag_config("status", foreground="gray")
    output_text.tag_config("error", foreground="red")

    def do_generate() -> None:
        keyword = entry_keyword.get().strip()
        if not keyword:
            messagebox.showwarning("입력 필요", "키워드를 입력해 주세요.")
            return

        path = selected_file_path.get().strip()
        reference_text = read_reference_file(path) if path else ""
        perspective = text_perspective.get("1.0", tk.END).strip()
        style = style_var.get()

        def work() -> None:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "연결 및 생성 중입니다...\n", "status")
            output_text.update()

            client = get_client()
            if client is None:
                root.after(
                    0,
                    lambda: _show_error(
                        "API 키 없음",
                        ".env 파일에 OPENAI_API_KEY를 설정해 주세요.\n.env.example을 참고하세요.",
                    ),
                )
                return

            try:
                content = generate_blog_post(
                    client, keyword, reference_text, perspective, style
                )
                root.after(0, lambda: _show_result(content))
            except Exception as e:
                root.after(0, lambda: _show_error("생성 오류", str(e)))

        def _show_error(title: str, msg: str) -> None:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"오류: {msg}\n", "error")
            messagebox.showerror(title, msg)

        def _show_result(content: str) -> None:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, content)

        threading.Thread(target=work, daemon=True).start()

    tk.Button(
        frame_btn,
        text="블로그 글 생성",
        command=do_generate,
        font=("", 10),
        width=14,
        cursor="hand2",
    ).pack(side=tk.LEFT)

    root.mainloop()


if __name__ == "__main__":
    run_app()
