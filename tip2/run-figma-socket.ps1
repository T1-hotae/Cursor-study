# Talk To Figma WebSocket 서버 실행 (Windows)
# 새로 설치한 Bun 사용: C:\Users\USER\.bun\bin\bun.exe

$Bun = "C:\Users\USER\.bun\bin\bun.exe"
$RepoDir = "cursor-talk-to-figma-mcp"
$RepoUrl = "https://github.com/grab/cursor-talk-to-figma-mcp.git"

if (-not (Test-Path $Bun)) {
    Write-Host "Bun이 없습니다. 먼저 설치하세요: powershell -c `"irm bun.sh/install.ps1|iex`"" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $RepoDir)) {
    Write-Host "저장소 클론 중..." -ForegroundColor Yellow
    git clone $RepoUrl $RepoDir
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

Set-Location $RepoDir
if (-not (Test-Path "node_modules")) {
    Write-Host "의존성 설치 중..." -ForegroundColor Yellow
    & $Bun install
}
Write-Host "WebSocket 서버 시작 (포트 3055). 종료하려면 Ctrl+C" -ForegroundColor Green
& $Bun socket
