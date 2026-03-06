# 고객 리뷰 데이터 분석 보고서 생성기

엑셀 파일의 고객 리뷰 데이터를 **컬럼명 기반**으로 읽어 분석한 뒤, ChatGPT API로 보고서를 생성합니다.

## 주요 컬럼 (컬럼명으로 찾음)

- **고객 리뷰**: `리뷰내용`
- **평점**: `평점`

그 외 컬럼(고객ID, 고객명, 노트북명, 구매일자, 사용기간, 만족도 등)도 분석·보고서에 참고됩니다.

## 사용 방법

1. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **API 키 설정**  
   프로젝트 폴더에 `.env` 파일을 만들고 다음 한 줄을 넣으세요.
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   (`.env.example`을 복사한 뒤 `your_openai_api_key_here`를 실제 키로 바꿔도 됩니다.)

3. **실행**  
   - **GUI (권장)**: `run_gui.bat` 더블클릭 또는 `python gui.py`  
     - 창에서 **찾아보기**로 엑셀 파일(.xlsx)을 선택한 뒤 **보고서 생성**을 누르면, 선택한 엑셀과 같은 폴더에 `리뷰_분석_보고서.md`로 저장됩니다.
   - **콘솔**: 같은 폴더에 엑셀 파일을 두고 `run.bat` 또는 `python main.py`

4. **결과**  
   `리뷰_분석_보고서.md` 파일이 생성됩니다.

## 사용 모델

- 보고서 생성: **gpt-4o-mini** (비용·품질 균형)  
- 더 높은 품질이 필요하면 `config.py`에서 `REPORT_MODEL = "gpt-4o"` 로 변경할 수 있습니다.

## 파일 구성

- `gui.py` - **GUI 실행** (엑셀 선택 → 보고서 생성 → 마크다운 저장)
- `main.py` - 콘솔 실행 진입점
- `config.py` - 주요 컬럼명, 모델 설정
- `excel_loader.py` - 컬럼명 기반 엑셀 로드
- `analyzer.py` - 평점·리뷰 통계 분석
- `report_generator.py` - OpenAI API로 보고서 문단 생성
- `run_gui.bat` - GUI 실행 (Windows)
