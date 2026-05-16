@echo off
chcp 65001 >nul
title Game Guide Platform

echo ========================================
echo    游戏攻略平台 - 启动脚本
echo ========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python
    pause
    exit /b 1
)

:: 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)

:: 关闭可能占用端口的进程
echo [准备] 检查端口占用...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo     关闭占用 8000 端口的进程 PID:%%a
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    echo     关闭占用 5173 端口的进程 PID:%%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo [1/3] 检查后端依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo     安装缺失的后端依赖...
    pip install -r "%~dp0backend\requirements.txt"
) else (
    echo     [OK] 后端依赖已就绪
)

echo.
echo [2/3] 检查前端依赖...
if not exist "%~dp0frontend\node_modules" (
    echo     正在安装前端依赖...
    cd /d "%~dp0frontend"
    call npm install
) else (
    echo     [OK] 前端依赖已就绪
)

echo.
echo [3/3] 启动服务...
echo.

:: 启动后端
start "后端服务 (FastAPI)" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0"

:: 等待后端启动
echo     等待后端服务启动...
timeout /t 2 >nul

:: 启动前端
start "前端服务 (Vite)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo    服务已启动！
echo ========================================
echo.
echo    前端: http://localhost:5173
echo    后端: http://localhost:8000
echo    API文档: http://localhost:8000/docs
echo.
echo    关闭此窗口不会停止服务
echo    如需停止服务，请关闭对应的命令行窗口
echo ========================================
pause
