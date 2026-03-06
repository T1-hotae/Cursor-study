# PDF 텍스트 추출기

현재 폴더에 있는 모든 PDF 파일에서 텍스트를 추출하는 프로그램입니다. **pdfplumber**를 사용합니다.

## 설치

```bash
pip install -r requirements.txt
```

또는

```bash
pip install pdfplumber
```

## 사용법

```bash
# 현재 폴더의 PDF 목록과 텍스트 미리보기 출력 (저장 여부는 실행 후 입력)
python pdf_text_extractor.py

# 미리보기 후 자동으로 extracted_text 폴더에 .txt 파일 저장
python pdf_text_extractor.py --save
python pdf_text_extractor.py -s
```

- **실행 위치**: 스크립트가 있는 폴더(`pj22`)의 PDF만 검색합니다.
- **저장 위치**: `extracted_text` 폴더에 `파일명_extracted.txt` 형식으로 저장됩니다.
- 스캔된 이미지 PDF는 텍스트가 추출되지 않을 수 있습니다 (OCR 필요).

---

## PDF 요약 (GPT)

`pdf_summarizer.py`는 현재 폴더의 PDF를 **OpenAI gpt-4o-mini**로 요약해 `summaries` 폴더에 저장합니다.

### 설치

```bash
pip install -r requirements.txt
```

### API 키 설정

**API 키는 코드에 넣지 말고 환경 변수로만 설정하세요.**

- **PowerShell**: `$env:OPENAI_API_KEY="your-api-key"`
- **CMD**: `set OPENAI_API_KEY=your-api-key`

### 실행

```bash
python pdf_summarizer.py
```

요약 파일은 `summaries/파일명_summary.txt` 형식으로 저장됩니다.
