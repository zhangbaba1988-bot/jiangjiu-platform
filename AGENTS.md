# 酱酒研学平台 (Jiangjiu Research Platform)

## Architecture
- Backend: Python FastAPI on port 8000, in-memory mode (no MongoDB/Redis)
- Frontend: Vue 3 + Vite on port 3001, Element Plus + Vant UI
- API proxy: Vite proxies /api/* to http://localhost:8000

## Project Structure
```
/Users/zhangbing/Downloads/jiangjiu-platform-final/
├── backend/
│   ├── app/main.py          # FastAPI app with full API endpoints
│   ├── app/database.py      # DB connections (gracefully falls back to memory)
│   └── data/                # JSON data files for memory mode
│       ├── knowledge.json   # 5 articles
│       ├── production.json  # 4 regions
│       ├── wineries.json    # 6 wineries
│       └── news.json        # 8 news items
├── frontend/
│   ├── src/api/index.js     # Axios API service (already complete, all endpoints)
│   ├── src/views/           # Vue page components (USING HARDCODED MOCK DATA)
│   └── vite.config.js       # Port 3001, /api proxy to :8000
└── config/
    └── frontend.env         # VITE_API_BASE_URL = http://localhost:8000
```

## How to Run
- Backend: `cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Frontend: `cd frontend && npm run dev`
- Both are currently running

## API Endpoints (backend)
- GET /knowledge?category=&page=&page_size=  → {code, data: {list, total, page, page_size}}
- GET /knowledge/categories → {code, data: [...]}
- GET /knowledge/:id → {code, data: {...}}
- GET /production?page=&page_size= → {code, data: {list, total, page, page_size}}
- GET /production/statistics → {code, data: {...}}
- GET /production/:id → {code, data: {...}}
- GET /wineries?production=&page=&page_size= → {code, data: {list, total, page, page_size}}
- GET /wineries/:id → {code, data: {...}}
- GET /news?type=&page=&page_size= → {code, data: {list, total, page, page_size}}
- GET /news/:id → {code, data: {...}}
- GET /search?keyword= → {code, data: {keyword, knowledge, wineries, production, news, total}}
- GET /search/hot → {code, data: [...]}
- GET /user/profile → {code, data: {...}}
- GET /user/favorites → {code, data: {list, total}}
- POST /user/favorites → {code, data: {success, message}}
- DELETE /user/favorites/:id → {code, data: {success, message}}
- GET /user/history → {code, data: {list, total}}

## API Response Format
All responses: { code: 200, message: "success", data: ... }

## Frontend API Module (already imported in each view)
```javascript
import { knowledgeApi, productionApi, wineryApi, newsApi, searchApi, userApi } from '@/api'
```
- knowledgeApi.getList(params), .getDetail(id), .getCategories()
- productionApi.getList(params), .getDetail(id), .getStatistics()
- wineryApi.getList(params), .getDetail(id)
- newsApi.getList(params), .getDetail(id)
- searchApi.search(keyword), .getHotSearches()
- userApi.getProfile(), .getFavorites(), .addFavorite(data), .removeFavorite(id), .getHistory()

## Current State - ALL Vue pages use hardcoded mock data
Every page in frontend/src/views/ has data hardcoded inside <script setup>:
- Knowledge.vue: articles grouped by category (culture/craft/tasting) hardcoded
- Wineries.vue: winery data hardcoded
- Production.vue: production zone data hardcoded  
- News.vue: news articles hardcoded
- Profile.vue: user profile hardcoded
- Search.vue: search results hardcoded
- KnowledgeDetail.vue, WineryDetail.vue, NewsDetail.vue, ProductionDetail.vue: detail content hardcoded

## UI Style Convention
- Color: gold/amber (#D4AF37) and brown (#8B4513)
- Cards with white background, 12px border-radius, shadow
- Icons displayed as emoji characters
- Category filter buttons with rounded style
- Grid layout: 3 columns on desktop
