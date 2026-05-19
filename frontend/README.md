# 酱酒研学平台 - 前端应用

基于 Vue 3 + Vite 构建的酱酒知识研学平台，涵盖酱酒文化、酿造工艺、产区数据、酒厂名录等全方位内容。

## 技术栈

- **框架**: Vue 3 + Vite
- **UI组件库**: Element Plus (PC端) + Vant 4 (移动端响应式适配)
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP请求**: Axios
- **图表**: ECharts
- **样式**: SCSS

## 功能特性

### 1. 首页
- 顶部Banner展示平台标语
- 核心数据看板（文章总数、产区数量、酒厂数量等）
- 快捷入口导航
- 推荐内容轮播
- 最新资讯列表

### 2. 知识库
- 分类导航（酱酒文化、酿造工艺、品鉴指南、产区介绍）
- 文章卡片式展示
- 支持筛选和搜索
- 文章详情页 + 相关推荐

### 3. 产区数据
- 交互式地图展示产区分布
- 产区详情（基本信息、年产量/产值统计、代表酒厂）
- 数据筛选功能
- ECharts可视化图表（趋势图、对比柱状图）

### 4. 酒厂名录
- 酒厂卡片列表
- 按地区、规模、品牌价值筛选
- 酒厂详情页（基本信息、代表产品、历史沿革、品牌故事）
- 搜索功能

### 5. 行业资讯
- 时间轴形式展示资讯列表
- 分类标签（政策动态、行业趋势、企业新闻、展会活动）
- 资讯详情页

### 6. 个人中心
- 用户信息展示
- 收藏文章列表
- 浏览历史
- 学习进度记录

## 快速开始

### 环境要求

- Node.js >= 16.x
- npm >= 8.x 或 yarn >= 1.22.x 或 pnpm >= 7.x

### 安装依赖

```bash
npm install
# 或
yarn install
# 或
pnpm install
```

### 开发模式

```bash
npm run dev
# 或
yarn dev
# 或
pnpm dev
```

访问 `http://localhost:5173` 查看应用

### 生产构建

```bash
npm run build
# 或
yarn build
# 或
pnpm build
```

构建产物将输出到 `dist` 目录

### 预览生产构建

```bash
npm run preview
# 或
yarn preview
# 或
pnpm preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API请求封装
│   │   └── index.js
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   │   └── layout/       # 布局组件
│   │       ├── AppHeader.vue
│   │       ├── AppFooter.vue
│   │       └── MobileNav.vue
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── stores/           # Pinia状态管理
│   │   └── user.js
│   ├── styles/           # 全局样式
│   │   ├── variables.scss
│   │   └── main.scss
│   ├── views/            # 页面组件
│   │   ├── Home.vue
│   │   ├── Knowledge.vue
│   │   ├── KnowledgeDetail.vue
│   │   ├── Production.vue
│   │   ├── Wineries.vue
│   │   ├── News.vue
│   │   ├── NewsDetail.vue
│   │   ├── Profile.vue
│   │   └── Search.vue
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── index.html            # HTML模板
├── vite.config.js        # Vite配置
├── package.json          # 项目依赖
└── README.md             # 项目说明
```

## 响应式设计

项目采用移动端优先的响应式设计策略：

- **移动端** (< 768px): Vant组件库 + 底部导航
- **平板** (768px - 1199px): 混合布局
- **桌面** (>= 1200px): Element Plus组件库 + 顶部导航

## 配色方案

- **主色调**: 深棕色 (#8B4513) - 代表酱酒的醇厚和传统
- **辅助色**: 金色 (#D4AF37) - 代表酱酒的珍贵和品质
- **背景色**: 米白色 (#FAF8F5) - 营造传统文化氛围
- **文字色**: 深灰色 (#333333) 保证可读性

## 部署说明

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    # Vue Router history模式
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api {
        proxy_pass http://backend-server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Docker 部署

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 后续优化建议

1. **性能优化**
   - 实现图片懒加载
   - 路由懒加载优化
   - 开启Gzip压缩
   - 使用CDN加速静态资源

2. **功能增强**
   - 添加用户评论系统
   - 实现文章分享功能
   - 添加数据导出功能
   - 开发移动端APP

3. **用户体验**
   - 添加深色模式
   - 实现离线缓存（PWA）
   - 优化首屏加载速度
   - 添加骨架屏加载效果

4. **代码质量**
   - 添加单元测试（Vitest）
   - 集成E2E测试
   - 代码规范检查（ESLint + Prettier）
   - 提交规范（Husky + Commitlint）

## 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 许可证

MIT
