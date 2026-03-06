# Talk To Figma 플러그인 – 서버 연결 방법

플러그인에서 **"Disconnected from server"** 가 나오면, WebSocket 서버를 터미널에서 먼저 실행한 뒤 Figma에서 포트로 연결해야 합니다.

## 1. WebSocket 서버 실행 (둘 중 하나 선택)

### Windows: `bunx` 오류가 날 때

`bunx cursor-talk-to-figma-socket` 실행 시 **'/bin/sh.exe'를 찾을 수 없음** 이 나오는 이유는, npm에 등록된 `bunx.ps1`이 Linux용 경로(`/bin/sh`)를 쓰기 때문입니다. **방금 설치한 Bun**은 `C:\Users\USER\.bun\bin\bun.exe` 에 있으므로, 아래처럼 **저장소에서 직접 실행**하는 방법을 쓰세요.

### 방법 A: 저장소에서 실행 (Windows 권장)

**한 번에 실행 (스크립트):**  
`tip2` 폴더에서:

```powershell
.\run-figma-socket.ps1
```

(처음 실행 시 저장소 클론 + `bun install` 후 소켓이 실행됩니다. 터미널을 닫지 마세요.)

**직접 실행:**  
1. 저장소 클론 후 이동:
   ```powershell
   git clone https://github.com/grab/cursor-talk-to-figma-mcp.git
   cd cursor-talk-to-figma-mcp
   ```
2. **새로 설치한 Bun**으로 의존성 설치 및 소켓 실행 (Windows에서 `bun`이 npm 쪽이면 전체 경로 사용):
   ```powershell
   C:\Users\USER\.bun\bin\bun.exe install
   C:\Users\USER\.bun\bin\bun.exe socket
   ```
3. **이 터미널 창을 닫지 말고** 그대로 두세요.

### 방법 B: PATH에 새 Bun을 먼저 두고 사용

시스템/사용자 환경 변수 **Path**에 `C:\Users\USER\.bun\bin` 을 **npm 경로보다 위**에 추가한 뒤 터미널을 다시 열면, `bun` / `bun x` 가 새로 설치한 Bun을 사용합니다. 그다음 저장소에서 `bun install` → `bun socket` 으로 실행하면 됩니다.

## 2. 포트 확인

- 기본 포트: **3055**
- 서버가 정상 기동되면 터미널에 WebSocket 서버 주소(예: `ws://localhost:3055`)가 출력됩니다.

## 3. Figma 플러그인에서 연결

1. Figma에서 **Talk To Figma** 플러그인 실행
2. 포트 번호 입력: **3055** (기본값)
3. **Connect** 클릭

## 4. Cursor MCP 설정 확인

Cursor가 Figma와 대화하려면 MCP 서버 설정이 필요합니다.

- **설정 위치**: `~/.cursor/mcp.json` (또는 프로젝트 MCP 설정)
- **예시**:
  ```json
  {
    "mcpServers": {
      "TalkToFigma": {
        "command": "bunx",
        "args": ["cursor-talk-to-figma-mcp@latest"]
      }
    }
  }
  ```
- Cursor를 재시작한 뒤, 위에서 실행한 **소켓 서버**와 **Figma 플러그인 연결**이 모두 유지된 상태에서 사용하세요.

## 요약

| 단계 | 할 일 |
|------|--------|
| 1 | 터미널에서 `bun socket` 또는 `bunx cursor-talk-to-figma-socket` 로 **WebSocket 서버 실행** (기본 포트 3055) |
| 2 | Figma 플러그인에서 포트 **3055** 로 **Connect** |
| 3 | Cursor MCP에 **TalkToFigma** 서버 설정 후 Cursor 재시작 |

- GitHub: [grab/cursor-talk-to-figma-mcp](https://github.com/grab/cursor-talk-to-figma-mcp)
- 플러그인 버전: 1.1.0
