#!/bin/bash
# 酱酒研学平台后端启动脚本

echo "========================================"
echo "  酱酒研学平台 - 后端服务启动"
echo "========================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "✗ 未找到Python3，请先安装Python"
    exit 1
fi

echo "✓ Python环境检查通过"

# 检查并安装依赖
echo ""
echo "检查依赖..."
pip3 install -q -r requirements.txt
echo "✓ 依赖安装完成"

# 生成模拟数据
echo ""
echo "生成模拟数据..."
python3 scripts/generate_mock_data.py
echo "✓ 模拟数据生成完成"

# 启动服务
echo ""
echo "启动后端API服务..."
echo "访问地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"
echo ""

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
