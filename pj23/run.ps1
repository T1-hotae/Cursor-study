# 고객 리뷰 분석 보고서 생성 - PowerShell 실행 스크립트
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "고객 리뷰 분석 보고서 생성 실행" -ForegroundColor Cyan
Write-Host ""

python main.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Read-Host "종료하려면 Enter 키를 누르세요"
    exit $LASTEXITCODE
}

Write-Host ""
Read-Host "종료하려면 Enter 키를 누르세요"
