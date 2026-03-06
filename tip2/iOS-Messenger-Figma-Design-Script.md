# iOS 스타일 메신저 앱 Figma 디자인 스크립트

**채널:** `y64bwhk3` (현재 연결된 채널)

TalkToFigma MCP가 연결된 상태에서 아래 순서대로 MCP 도구를 호출하면 iOS 메시지 앱과 같은 기본 메신저 화면이 Figma에 생성됩니다.

---

## 사전 조건

1. **WebSocket 서버 실행**  
   `cursor-talk-to-figma-mcp` 폴더에서 `.\run-socket.ps1` 실행 (포트 3055).

2. **Figma 플러그인**  
   Figma에서 Talk To Figma MCP 플러그인 실행 → 채널 `y64bwhk3` 입력 후 **Connect**.

3. **Cursor MCP**  
   Cursor 설정에서 TalkToFigma MCP 서버가 정상 연결되어 있어야 합니다.  
   (에러 시: Cursor 설정 → MCP에서 서버 상태 확인)

---

## MCP 도구 호출 순서 (iOS 메신저)

### 1. 채널 연결

- **도구:** `join_channel`
- **인자:** `{ "channel": "y64bwhk3" }`

---

### 2. 메인 화면 프레임 (iPhone 14 크기)

- **도구:** `create_frame`
- **인자:**
  - `x`: 0, `y`: 0
  - `width`: 390, `height`: 844
  - `name`: "iOS Messenger"
  - `fillColor`: `{ "r": 1, "g": 1, "b": 1, "a": 1 }` (흰색)
- **반환값의 `id`**를 메인 프레임 `parentId`로 사용 (아래 단계에서 `MAIN_FRAME_ID`로 표기).

---

### 3. 상단 네비게이션 바 (iOS 스타일)

- **도구:** `create_frame`
- **인자:**
  - `x`: 0, `y`: 47 (상태바 아래)
  - `width`: 390, `height`: 44
  - `name`: "Nav Bar"
  - `parentId`: `MAIN_FRAME_ID`
  - `fillColor`: `{ "r": 0.95, "g": 0.95, "b": 0.97, "a": 1 }` (#F2F2F7)
  - `layoutMode`: "HORIZONTAL"
  - `primaryAxisAlignItems`: "CENTER"
  - `counterAxisAlignItems`: "CENTER"
  - `paddingLeft`: 16, `paddingRight`: 16, `paddingTop`: 8, `paddingBottom`: 8
- **반환값의 `id`** → `NAV_BAR_ID`

---

### 4. 네비게이션 타이틀 "Messages"

- **도구:** `create_text`
- **인자:**
  - `x`: 0, `y`: 0 (부모 내에서 오토레이아웃으로 배치)
  - `text`: "Messages"
  - `fontSize`: 17
  - `fontWeight`: 600
  - `fontColor`: `{ "r": 0, "g": 0, "b": 0, "a": 1 }`
  - `name`: "Nav Title"
  - `parentId`: `NAV_BAR_ID`

---

### 5. 채팅 영역 (스크롤 영역 배경)

- **도구:** `create_frame`
- **인자:**
  - `x`: 0, `y`: 91 (네비바 아래)
  - `width`: 390, `height`: 652
  - `name`: "Chat Area"
  - `parentId`: `MAIN_FRAME_ID`
  - `fillColor`: `{ "r": 1, "g": 1, "b": 1, "a": 1 }`
- **반환값의 `id`** → `CHAT_AREA_ID`

---

### 6. 받은 메시지 말풍선 (왼쪽, 회색)

- **도구:** `create_frame`
- **인자:**
  - `x`: 16, `y`: 24
  - `width`: 240, `height`: 48
  - `name`: "Bubble Received"
  - `parentId`: `CHAT_AREA_ID`
  - `fillColor`: `{ "r": 0.9, "g": 0.9, "b": 0.92, "a": 1 }` (#E5E5EA)
  - `layoutMode`: "HORIZONTAL"
  - `paddingLeft`: 12, `paddingRight`: 12, `paddingTop`: 8, `paddingBottom`: 8
- **반환값의 `id`** → `BUBBLE_RECEIVED_ID`

- **도구:** `set_corner_radius`  
  - `nodeId`: `BUBBLE_RECEIVED_ID`, `radius`: 18

- **도구:** `create_text`
  - `x`: 0, `y`: 0
  - `text`: "안녕, 뭐 해?"
  - `fontSize`: 16
  - `fontWeight`: 400
  - `fontColor`: `{ "r": 0, "g": 0, "b": 0, "a": 1 }`
  - `name`: "Message Text"
  - `parentId`: `BUBBLE_RECEIVED_ID`

---

### 7. 보낸 메시지 말풍선 (오른쪽, 파란색)

- **도구:** `create_frame`
- **인자:**
  - `x`: 134, `y`: 88 (받은 말풍선 아래)
  - `width`: 240, `height`: 48
  - `name`: "Bubble Sent"
  - `parentId`: `CHAT_AREA_ID`
  - `fillColor`: `{ "r": 0, "g": 0.478, "b": 1, "a": 1 }` (#007AFF iOS Blue)
  - `layoutMode`: "HORIZONTAL"
  - `paddingLeft`: 12, `paddingRight`: 12, `paddingTop`: 8, `paddingBottom`: 8
- **반환값의 `id`** → `BUBBLE_SENT_ID`

- **도구:** `set_corner_radius`  
  - `nodeId`: `BUBBLE_SENT_ID`, `radius`: 18

- **도구:** `create_text`
  - `x`: 0, `y`: 0
  - `text`: "잘 지내! 나도 바쁘게 일 중이야."
  - `fontSize`: 16
  - `fontWeight`: 400
  - `fontColor`: `{ "r": 1, "g": 1, "b": 1, "a": 1 }`
  - `name`: "Message Text"
  - `parentId`: `BUBBLE_SENT_ID`

---

### 8. 하단 입력 영역 (iOS 스타일)

- **도구:** `create_frame`
- **인자:**
  - `x`: 0, `y`: 743
  - `width`: 390, `height`: 101 (Safe Area 포함)
  - `name`: "Input Bar"
  - `parentId`: `MAIN_FRAME_ID`
  - `fillColor`: `{ "r": 0.95, "g": 0.95, "b": 0.97, "a": 1 }`
  - `layoutMode`: "HORIZONTAL"
  - `primaryAxisAlignItems`: "CENTER"
  - `counterAxisAlignItems`: "CENTER"
  - `itemSpacing`: 8
  - `paddingLeft`: 8, `paddingRight`: 8, `paddingTop`: 8, `paddingBottom`: 34 (홈 인디케이터 영역)
- **반환값의 `id`** → `INPUT_BAR_ID`

---

### 9. 입력 필드 (텍스트 입력창)

- **도구:** `create_frame`
- **인자:**
  - `x`: 0, `y`: 0
  - `width`: 300, `height`: 36
  - `name`: "Message Input"
  - `parentId`: `INPUT_BAR_ID`
  - `fillColor`: `{ "r": 1, "g": 1, "b": 1, "a": 1 }`
  - `layoutMode`: "HORIZONTAL"
  - `paddingLeft`: 12, `paddingRight`: 12, `paddingTop`: 8, `paddingBottom`: 8
- **반환값의 `id`** → `INPUT_FIELD_ID`

- **도구:** `set_corner_radius`  
  - `nodeId`: `INPUT_FIELD_ID`, `radius`: 18

- **도구:** `create_text`
  - `x`: 0, `y`: 0
  - `text`: "iMessage"
  - `fontSize`: 16
  - `fontWeight`: 400
  - `fontColor`: `{ "r": 0.56, "g": 0.56, "b": 0.58, "a": 1 }` (placeholder gray)
  - `name`: "Placeholder"
  - `parentId`: `INPUT_FIELD_ID`

---

### 10. 전송 버튼

- **도구:** `create_frame`
- **인자:**
  - `x`: 0, `y`: 0
  - `width`: 32, `height`: 32
  - `name`: "Send Button"
  - `parentId`: `INPUT_BAR_ID`
  - `fillColor`: `{ "r": 0, "g": 0.478, "b": 1, "a": 1 }`
- **반환값의 `id`** → `SEND_BTN_ID`

- **도구:** `set_corner_radius`  
  - `nodeId`: `SEND_BTN_ID`, `radius`: 16

- **도구:** `create_text`
  - `x`: 0, `y`: 0
  - `text`: "↑"
  - `fontSize`: 18
  - `fontWeight`: 600
  - `fontColor`: `{ "r": 1, "g": 1, "b": 1, "a": 1 }`
  - `name`: "Send Icon"
  - `parentId`: `SEND_BTN_ID`

---

## 실행 방법

1. MCP가 정상 연결된 상태에서 Cursor 채팅에서  
   **"채널 y64bwhk3에 연결하고, iOS 메신저 앱 디자인 스크립트대로 Figma에 만들어줘"** 라고 요청하거나,
2. 위 순서대로 각 MCP 도구를 호출하면서, 반환된 `id`를 다음 단계의 `parentId`에 넣어 실행합니다.

---

## MCP 서버가 에러일 때

- **Cursor 설정 → MCP** 에서 TalkToFigma 서버 상태를 확인하세요.
- WebSocket 서버(`run-socket.ps1`)와 Figma 플러그인(채널 `9kogsi4q` 연결)이 켜져 있어야 MCP가 정상 동작할 수 있습니다.
- 서버를 재시작하거나 Cursor를 재시작한 뒤 다시 시도해 보세요.
