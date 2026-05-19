# 酱酒研学平台

## 项目简介

酱酒研学平台是一个集酱酒文化传播、知识学习、产区数据展示、酒厂信息查询于一体的综合性知识平台。

## 目录结构

```
酱酒研学平台/
├── backend/          # 后端API服务
├── frontend/         # 前端项目（Vue3版本）
├── static-site/      # 静态网站版本
├── spider/           # 爬虫系统
├── scheduler/        # 定时任务
├── screenshots/      # 页面截图
├── images/           # 项目图片资源
├── config/           # 配置文件
├── start_all.sh      # 一键启动脚本
├── stop_all.sh       # 停止服务脚本
└── README.md         # 项目说明
```

## 快速开始

### 一键启动
```bash
chmod +x start_all.sh
./start_all.sh
```

### 分别启动

1. 启动后端服务：
```bash
cd backend
pip install -r requirements.txt
cd app && python main.py
```

2. 启动前端服务：
```bash
cd frontend
npm install
npm run dev
```

3. 启动爬虫：
```bash
cd spider
python main.py
```

## 技术栈

- **后端**: Python FastAPI + SQLite
- **前端**: Vue 3 + Vite + Element Plus
- **爬虫**: Python Requests + BeautifulSoup
- **定时任务**: APScheduler

## 功能模块

1. 知识库系统 - 酱酒文化、酿造工艺、品鉴指南
2. 产区数据 - 交互式地图、数据可视化
3. 酒厂名录 - 企业信息、品牌故事
4. 行业资讯 - 政策动态、市场趋势
5. 数据爬虫 - 天眼查API、市场监管局数据
6. 定时任务 - 数据同步、内容更新

## 文档

- 需求分析文档.md
- 技术方案文档.md
- 项目架构总结.md
- 前后端联调指南.md
- 服务启动报告.md

## 许可证

MIT

