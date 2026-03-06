# 한국 주식 가격 TOP 50 대시보드

금융위원회 주식시세정보 API를 사용해 **종가 기준 가격이 높은 순** 상위 50개 종목을 표시하는 대시보드입니다.

## 실행 방법

1. Node.js가 설치되어 있어야 합니다.
2. 터미널에서 프로젝트 폴더로 이동 후:

```bash
node server.js
```

3. 브라우저에서 **http://localhost:3000** 을 엽니다.

## 구성

- **index.html** – 대시보드 화면 (HTML + CSS + JavaScript)
- **server.js** – 로컬 서버 + API 프록시 (CORS 회피용)

## API

- 공공데이터포털 **금융위원회_주식시세정보** (getStockPriceInfo)
- 기준일자 당일 데이터를 불러와 종가(`clpr`) 기준 내림차순 정렬 후 상위 50개만 표시합니다.
