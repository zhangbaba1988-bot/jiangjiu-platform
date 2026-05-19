#!/bin/bash
# 酱酒研学平台爬虫启动脚本

echo "============================================================"
echo "  酱酒研学平台爬虫系统启动"
echo "============================================================"

cd "$(dirname "$0")/spider"

echo ""
echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python"
    exit 1
fi

echo ""
echo "正在安装依赖..."
pip3 install -r requirements.txt

echo ""
echo "正在验证环境..."
python3 test_spider.py

echo ""
echo "============================================================"
echo "是否开始抓取？(y/n)"
read answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo ""
    echo "开始抓取所有数据源..."
    python3 main.py
    echo ""
    echo "抓取完成！"
    echo "日志文件: ../爬虫抓取日志.md"
    echo "报告文件: ../数据抓取统计报告.md"
else
    echo ""
    echo "已取消抓取。"
    echo "如需运行单个数据源，请使用: python3 main.py --source <数据源ID>"
    echo "数据源列表: python3 main.py --list"
fi

echo ""
echo "============================================================"
