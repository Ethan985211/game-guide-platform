@echo off
chcp 65001 >nul
color 0A

echo ========================================
echo   游戏攻略平台 - 开发环境启动
echo ========================================
echo.

:: 检查端口占用
echo [准备] 检查端口占用...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo     关闭占用 8000 端口的进程...
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    echo     关闭占用 5173 端口的进程...
    taskkill /F /PID %%a >nul 2>&1
)

cd /d "%~dp0backend"
echo.
echo [后端] 安装依赖并启动...
pip install -q -r requirements.txt 2>nul
start "Backend" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

cd /d "%~dp0frontend"
echo.
echo [前端] 安装依赖并启动...
if not exist "node_modules" (
    call npm install
)
start "Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo   服务已启动！
echo ========================================
echo   前端: http://localhost:5173
echo   后端: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo ========================================
echo.
echo 按任意键退出此窗口（服务继续运行）...
pause >nul
