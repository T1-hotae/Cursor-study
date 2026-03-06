@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 고객 리뷰 분석 보고서 생성 실행
echo.

python main.py
if errorlevel 1 (
    echo.
    pause
    exit /b 1
)

echo.
pause
