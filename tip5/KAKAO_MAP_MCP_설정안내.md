# Kakao Map MCP 설정 안내

Cursor에서 **Kakao Map MCP**를 사용하려면 아래 순서대로 진행하세요.

## 1. 카카오 REST API 키 발급

1. [카카오 디벨로퍼스](https://developers.kakao.com/)에 접속 후 로그인
2. **내 애플리케이션** → **애플리케이션 추가하기**로 앱 생성
3. 생성한 앱 선택 → **앱 키** 메뉴에서 **REST API 키** 복사
4. **플랫폼** 메뉴에서 **Web** 플랫폼 등록 (필요 시)
5. **카카오맵**, **로컬**, **검색** 등 사용할 API를 **활성화** (제품 설정)

## 2. kakao-api-mcp-server 설치

**Node.js**가 설치되어 있어야 합니다. [nodejs.org](https://nodejs.org/)에서 설치하세요.

**PowerShell**을 **Windows 메뉴에서 직접 열고**(Cursor 내장 터미널이 아닌, 네트워크·캐시 제한이 없는 환경), 아래 중 하나를 실행하세요.

**방법 1 – 스크립트 한 번에 실행**

```powershell
cd C:\Users\USER\Desktop\cursor\tip5\kakao-api-mcp-server
.\build.ps1
```

**방법 2 – 수동 실행**

```powershell
cd C:\Users\USER\Desktop\cursor\tip5\kakao-api-mcp-server
npm install
```

- `npm install` 시 **"cache mode is 'only-if-cached'"** 오류가 나면 먼저 실행:  
  `npm config set prefer-offline false`  
  그다음 다시 `npm install` 실행.
- Cursor MCP 설정은 **`npx tsx`로 소스를 직접 실행**하므로, 위 설치만 끝나면 **별도 빌드(`npm run build`)는 필요 없습니다.**

## 3. Cursor MCP 설정에 API 키 입력

1. **Cursor** → **설정(Settings)** → **Features** → **MCP** 이동
2. **Kakao Map** 서버 항목에서 **편집(연필 아이콘)** 클릭
3. **Environment variables**에 `KAKAO_REST_API_KEY` 값에 발급받은 REST API 키 입력
   - 또는 `C:\Users\USER\.cursor\mcp.json`을 열어 `"KAKAO_REST_API_KEY"` 값에 키를 직접 입력

```json
"env": {
  "KAKAO_REST_API_KEY": "발급받은_REST_API_키"
}
```

4. 저장 후 Cursor를 재시작하거나 MCP 목록 새로고침

## 4. Kakao Map MCP가 동작하지 않을 때

1. **의존성 설치 확인**  
   Cursor **밖**에서 PowerShell을 열고 아래를 실행한 뒤, Cursor를 재시작하세요.
   ```powershell
   cd C:\Users\USER\Desktop\cursor\tip5\kakao-api-mcp-server
   npm config set prefer-offline false
   npm install
   ```
2. **REST API 키 확인**  
   [카카오 디벨로퍼스](https://developers.kakao.com/) → 내 애플리케이션 → 앱 키에서 **REST API 키**가 `mcp.json`의 `KAKAO_REST_API_KEY`와 같은지 확인하세요.
3. **Cursor 재시작**  
   설정 변경 후 **Cursor를 완전히 종료했다가 다시 실행**한 뒤, MCP 목록에서 Kakao Map이 켜져 있는지 확인하세요.

## 5. 서버 경로가 다른 경우

저장소를 다른 폴더에 클론했다면 `mcp.json`의 경로를 수정하세요.

- **파일 위치**: `C:\Users\USER\.cursor\mcp.json`
- **수정할 부분**: `args` 배열의 **세 번째** 항목(소스 경로)  
  `"C:\\Users\\USER\\Desktop\\cursor\\tip5\\kakao-api-mcp-server\\src\\index.ts"`  
  → 실제 `kakao-api-mcp-server\src\index.ts` 경로로 변경

## Kakao Map MCP로 할 수 있는 것

| 도구 | 설명 |
|------|------|
| **장소 검색** | 키워드로 카카오맵 장소 검색 (주소, 카테고리, 연락처) |
| **좌표→주소 변환** | 경위도 좌표를 도로명/지번 주소로 변환 |
| **길찾기** | 출발지→목적지 경로, 거리, 소요 시간, 택시 요금, 교통 정보 |
| **다음 웹 검색** | 웹 문서 검색 |
| **다음 이미지/블로그/카페 검색** | 키워드로 이미지, 블로그, 카페 글 검색 |

설정이 끝나면 채팅에서 예를 들어 **"판교역 근처 맛집 검색해줘"**, **"강남역에서 역삼역까지 차로 길찾기"**처럼 요청하면 Kakao Map MCP 도구가 사용됩니다.
