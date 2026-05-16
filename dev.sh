#!/bin/bash

# 游戏攻略平台 - 一键启动脚本

echo "========================================"
echo "  游戏攻略平台 - 开发环境启动"
echo "========================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查端口占用并清理
echo -e "${YELLOW}[准备] 检查端口占用...${NC}"
for port in 8000 5173; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ -n "$pid" ]; then
        echo -e "    关闭占用 $port 端口的进程 (PID: $pid)"
        kill -9 $pid 2>/dev/null
    fi
done

# 启动后端
echo -e "\n${YELLOW}[后端] 启动服务 (端口 8000)...${NC}"
cd backend
pip install -q -r requirements.txt 2>/dev/null
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo -e "${GREEN}[OK] 后端已启动 (PID: $BACKEND_PID)${NC}"

# 等待后端启动
sleep 2

# 启动前端
echo -e "\n${YELLOW}[前端] 启动服务 (端口 5173)...${NC}"
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "    安装前端依赖..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}[OK] 前端已启动 (PID: $FRONTEND_PID)${NC}"

echo ""
echo -e "${GREEN}========================================"
echo "  服务已启动！"
echo "========================================"
echo "  前端: http://localhost:5173"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo "========================================${NC}"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待退出信号
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
