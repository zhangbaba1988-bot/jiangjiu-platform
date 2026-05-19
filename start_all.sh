#!/bin/bash
# 酱酒研学平台前后端一键启动脚本

echo "========================================"
echo "  酱酒研学平台 - 前后端联调环境"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否已安装screen
if ! command -v screen &> /dev/null; then
    echo -e "${YELLOW}⚠ 未安装screen，将在前台分别启动服务${NC}"
    echo "请手动在两个终端分别运行:"
    echo "  cd backend && bash start.sh"
    echo "  cd frontend && bash start.sh"
    exit 1
fi

echo -e "${GREEN}✓ screen已安装${NC}"

# 停止已存在的会话
echo ""
echo "停止已存在的服务会话..."
screen -S jiangjiu-backend -X quit 2>/dev/null
screen -S jiangjiu-frontend -X quit 2>/dev/null
sleep 1

# 启动后端
echo ""
echo "启动后端服务..."
screen -dmS jiangjiu-backend bash -c "cd backend && bash start.sh"
sleep 3

# 检查后端是否启动成功
if screen -list | grep -q "jiangjiu-backend"; then
    echo -e "${GREEN}✓ 后端服务已启动${NC}"
    echo "  地址: http://localhost:8000"
    echo "  API文档: http://localhost:8000/docs"
else
    echo -e "${RED}✗ 后端服务启动失败${NC}"
fi

# 启动前端
echo ""
echo "启动前端服务..."
screen -dmS jiangjiu-frontend bash -c "cd frontend && bash start.sh"
sleep 3

# 检查前端是否启动成功
if screen -list | grep -q "jiangjiu-frontend"; then
    echo -e "${GREEN}✓ 前端服务已启动${NC}"
    echo "  地址: http://localhost:3000"
else
    echo -e "${RED}✗ 前端服务启动失败${NC}"
fi

echo ""
echo "========================================"
echo -e "${GREEN}  联调环境启动完成！${NC}"
echo "========================================"
echo ""
echo "服务管理命令:"
echo "  查看后端日志: screen -r jiangjiu-backend"
echo "  查看前端日志: screen -r jiangjiu-frontend"
echo "  退出查看: Ctrl+A, D"
echo "  停止所有服务: bash stop_all.sh"
echo ""
echo "访问地址:"
echo "  前端页面: http://localhost:3000"
echo "  后端API: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
