#!/bin/bash
# 酱酒研学平台前端启动脚本

echo "========================================"
echo "  酱酒研学平台 - 前端服务启动"
echo "========================================"

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "✗ 未找到Node.js，请先安装Node.js"
    exit 1
fi

echo "✓ Node.js环境检查通过"
echo "  Node版本: $(node -v)"
echo "  NPM版本: $(npm -v)"

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo ""
    echo "安装依赖..."
    npm install
    echo "✓ 依赖安装完成"
else
    echo "✓ 依赖已存在"
fi

# 启动开发服务器
echo ""
echo "启动前端开发服务器..."
echo "访问地址: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"
echo ""

npm run dev
