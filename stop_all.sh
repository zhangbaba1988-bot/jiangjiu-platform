#!/bin/bash
# 酱酒研学平台前后端停止脚本

echo "========================================"
echo "  酱酒研学平台 - 停止服务"
echo "========================================"

echo ""
echo "正在停止后端服务..."
screen -S jiangjiu-backend -X quit 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ 后端服务已停止"
else
    echo "⚠ 后端服务未运行或停止失败"
fi

echo ""
echo "正在停止前端服务..."
screen -S jiangjiu-frontend -X quit 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ 前端服务已停止"
else
    echo "⚠ 前端服务未运行或停止失败"
fi

echo ""
echo "========================================"
echo "  所有服务已停止"
echo "========================================"
echo ""
echo "当前screen会话列表:"
screen -list
echo ""
