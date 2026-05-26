from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import json
import os
import uuid

from app.database import get_db, mongodb_connected, redis_connected

app = FastAPI(
    title="酱酒研学平台API",
    description="酱酒研学平台后端API接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_data = {
    "knowledge": [],
    "production": [],
    "wineries": [],
    "news": []
}

if not mongodb_connected:
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    for name in memory_data:
        json_path = os.path.join(data_dir, f"{name}.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                memory_data[name] = json.load(f)


# 会员与收藏数据
sample_favorites = [
    {
        "id": "klg_001",
        "title": "酱酒历史溯源：从远古到现代的千年传承",
        "summary": "深入探索酱酒的起源与发展，从汉武帝枸酱酒到巴拿马金奖的传奇故事",
        "category": "culture",
        "icon": "📜"
    },
    {
        "id": "news_001",
        "title": "茅台集团2025年营收突破1800亿元",
        "summary": "茅台集团公布2025年度业绩报告，全年营收突破1800亿元，同比增长12%。",
        "type": "company",
        "source": "茅台集团",
        "icon": "📈"
    },
    {
        "id": "prd_001",
        "name": "茅台镇核心产区",
        "description": "中国酱酒的心脏，全球市值最高酒企所在地",
        "region": "贵州省仁怀市",
        "icon": "🏛️"
    }
]

sample_history = [
    {
        "id": "wry_001",
        "name": "贵州茅台酒厂",
        "production": "茅台镇核心产区",
        "brand": "贵州茅台",
        "description": "中国酱酒标杆，全球市值最高酒企。飞天茅台年销千亿。",
        "icon": "👑"
    },
    {
        "id": "klg_005",
        "title": "茅台镇：不可复制的微生物王国",
        "summary": "茅台核心产区已发现1946种微生物，两株全新菌种被命名为'石窖梭菌'和'茅台梭菌'",
        "category": "culture",
        "icon": "🔬"
    },
    {
        "id": "news_002",
        "title": "酱酒新国标正式实施 行业洗牌加速",
        "summary": "酱香型白酒国家标准修订版正式实施，对工艺标准、原料要求等做出更严格规定。",
        "type": "policy",
        "source": "市场监管总局",
        "icon": "📋"
    }
]

user_state = {
    "profile": {
        "id": "user_001",
        "nickname": "酱酒爱好者",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=jiangjiu",
        "favorite_count": len(sample_favorites),
        "history_count": len(sample_history)
    },
    "favorites": [json.loads(json.dumps(item)) for item in sample_favorites],
    "history": [json.loads(json.dumps(item)) for item in sample_history],
    "members": [
        {
            "id": "user_001",
            "nickname": "酱酒爱好者",
            "email": "user001@example.com",
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=jiangjiu",
            "status": "active",
            "register_time": "2026-01-10T08:00:00",
            "last_login": "2026-05-25T20:00:00",
            "favorite_count": len(sample_favorites),
            "history_count": len(sample_history)
        },
        {
            "id": "user_002",
            "nickname": "品鉴达人",
            "email": "user002@example.com",
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=jiangjiu2",
            "status": "active",
            "register_time": "2026-02-12T09:00:00",
            "last_login": "2026-05-24T17:30:00",
            "favorite_count": 5,
            "history_count": 12
        },
        {
            "id": "user_003",
            "nickname": "老酒收藏者",
            "email": "user003@example.com",
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=jiangjiu3",
            "status": "inactive",
            "register_time": "2026-03-20T11:20:00",
            "last_login": "2026-05-20T12:55:00",
            "favorite_count": 8,
            "history_count": 9
        }
    ]
}

admin_credentials = {
    "superadmin": "Jiangjiu@2026"
}
admin_tokens = set()


class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


def get_collection(name):
    if mongodb_connected:
        db = get_db()
        if db is not None:
            return db[name]
    return None


def find_documents(collection_name, query=None, limit=100, skip=0):
    if query is None:
        query = {}

    collection = get_collection(collection_name)
    if collection is not None:
        cursor = collection.find(query).skip(skip).limit(limit)
        result = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result

    data = memory_data[collection_name]
    if query:
        filtered = []
        for item in data:
            match = True
            for k, v in query.items():
                if isinstance(v, dict) and '$regex' in v:
                    import re
                    pattern = re.compile(v['$regex'], re.IGNORECASE)
                    if not pattern.search(str(item.get(k, ''))):
                        match = False
                        break
                elif item.get(k) != v:
                    match = False
                    break
            if match:
                filtered.append(item)
        return filtered[skip:skip+limit]

    return data[skip:skip+limit]


def count_documents(collection_name, query=None):
    if query is None:
        query = {}

    collection = get_collection(collection_name)
    if collection is not None:
        return collection.count_documents(query)

    items = memory_data.get(collection_name, [])
    if not query or query == {}:
        return len(items)

    return sum(1 for item in items if all(item.get(k) == v for k, v in query.items()))


def find_one(collection_name, query):
    results = find_documents(collection_name, query, limit=1)
    return results[0] if results else None


def sync_user_counts():
    user_state["profile"]["favorite_count"] = len(user_state["favorites"])
    user_state["profile"]["history_count"] = len(user_state["history"])

    for member in user_state["members"]:
        if member["id"] == user_state["profile"]["id"]:
            member["favorite_count"] = len(user_state["favorites"])
            member["history_count"] = len(user_state["history"])


def parse_bearer_token(authorization: Optional[str]):
    if not authorization:
        return None
    if not authorization.startswith("Bearer "):
        return None
    return authorization.replace("Bearer ", "", 1)


@app.get("/")
async def root():
    return ApiResponse(data={
        "service": "酱酒研学平台API",
        "version": "1.0.0",
        "mongodb": "connected" if mongodb_connected else "memory_mode",
        "redis": "connected" if redis_connected else "memory_mode"
    })


@app.get("/health")
async def health_check():
    return ApiResponse(data={
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.get("/dashboard")
async def get_dashboard():
    try:
        knowledge_count = count_documents("knowledge")
        production_count = count_documents("production")
        wineries_count = count_documents("wineries")
        news_count = count_documents("news")

        latest_news = find_documents("news", limit=5)
        hot_wineries = find_documents("wineries", limit=6)

        return ApiResponse(data={
            "statistics": {
                "knowledge_count": knowledge_count,
                "production_count": production_count,
                "wineries_count": wineries_count,
                "news_count": news_count
            },
            "latest_news": latest_news,
            "hot_wineries": hot_wineries
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge")
async def get_knowledge_list(
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000)
):
    try:
        query = {}
        if category:
            query["category"] = category

        skip = (page - 1) * page_size
        total = count_documents("knowledge", query)
        items = find_documents("knowledge", query, limit=page_size, skip=skip)

        return ApiResponse(data={
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge/categories")
async def get_knowledge_categories():
    categories = [
        {"id": "culture", "name": "酱酒文化", "count": 0},
        {"id": "craft", "name": "酿造工艺", "count": 0},
        {"id": "tasting", "name": "品鉴指南", "count": 0},
        {"id": "production", "name": "产区介绍", "count": 0}
    ]

    for cat in categories:
        cat["count"] = count_documents("knowledge", {"category": cat["id"]})

    return ApiResponse(data=categories)


@app.get("/knowledge/{item_id}")
async def get_knowledge_detail(item_id: str):
    item = find_one("knowledge", {"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="文章不存在")
    return ApiResponse(data=item)


@app.get("/production")
async def get_production_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000)
):
    try:
        skip = (page - 1) * page_size
        total = count_documents("production")
        items = find_documents("production", limit=page_size, skip=skip)

        return ApiResponse(data={
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/production/statistics")
async def get_production_statistics():
    productions = find_documents("production", limit=100)

    total_output = sum(p.get("output", 0) for p in productions)
    total_value = sum(p.get("output_value", 0) for p in productions)
    total_wineries = sum(p.get("winery_count", 0) for p in productions)

    return ApiResponse(data={
        "total_output": total_output,
        "total_value": total_value,
        "total_wineries": total_wineries,
        "productions": productions
    })


@app.get("/production/{item_id}")
async def get_production_detail(item_id: str):
    item = find_one("production", {"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="产区不存在")
    return ApiResponse(data=item)


@app.get("/wineries")
async def get_wineries_list(
    production: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000)
):
    try:
        query = {}
        if production:
            query["production"] = production

        skip = (page - 1) * page_size
        total = count_documents("wineries", query)
        items = find_documents("wineries", query, limit=page_size, skip=skip)

        return ApiResponse(data={
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/wineries/{item_id}")
async def get_winery_detail(item_id: str):
    item = find_one("wineries", {"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="酒厂不存在")
    return ApiResponse(data=item)


@app.get("/news")
async def get_news_list(
    type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000)
):
    try:
        query = {}
        if type:
            query["type"] = type

        skip = (page - 1) * page_size
        total = count_documents("news", query)
        items = find_documents("news", query, limit=page_size, skip=skip)

        return ApiResponse(data={
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/news/{item_id}")
async def get_news_detail(item_id: str):
    item = find_one("news", {"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="资讯不存在")
    return ApiResponse(data=item)


@app.get("/search")
async def search(keyword: str = Query(..., min_length=1)):
    try:
        query = {"$regex": keyword, "$options": "i"}

        knowledge_results = find_documents("knowledge", {"title": query}, limit=10)
        wineries_results = find_documents("wineries", {"name": query}, limit=10)
        production_results = find_documents("production", {"name": query}, limit=10)
        news_results = find_documents("news", {"title": query}, limit=10)

        return ApiResponse(data={
            "keyword": keyword,
            "knowledge": knowledge_results,
            "wineries": wineries_results,
            "production": production_results,
            "news": news_results,
            "total": len(knowledge_results) + len(wineries_results) + len(production_results) + len(news_results)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/hot")
async def get_hot_searches():
    hot_searches = [
        {"keyword": "坤沙工艺", "count": 1256},
        {"keyword": "茅台镇", "count": 1089},
        {"keyword": "酱酒品鉴", "count": 967},
        {"keyword": "12987", "count": 856},
        {"keyword": "赤水河", "count": 743},
        {"keyword": "核心产区", "count": 698},
        {"keyword": "收藏价值", "count": 621},
        {"keyword": "碎沙工艺", "count": 543}
    ]
    return ApiResponse(data=hot_searches)


@app.get("/user/profile")
async def get_user_profile():
    sync_user_counts()
    return ApiResponse(data=user_state["profile"])


@app.put("/user/profile")
async def update_user_profile(data: Dict[str, Any]):
    nickname = data.get("nickname")
    avatar = data.get("avatar")

    if nickname:
        user_state["profile"]["nickname"] = nickname
    if avatar:
        user_state["profile"]["avatar"] = avatar

    for member in user_state["members"]:
        if member["id"] == user_state["profile"]["id"]:
            if nickname:
                member["nickname"] = nickname
            if avatar:
                member["avatar"] = avatar

    sync_user_counts()
    return ApiResponse(data=user_state["profile"])


@app.get("/user/favorites")
async def get_user_favorites():
    sync_user_counts()
    return ApiResponse(data={
        "list": user_state["favorites"],
        "total": len(user_state["favorites"])
    })


@app.post("/user/favorites")
async def add_favorite(data: Dict[str, Any]):
    item_id = data.get("id")
    if not item_id:
        raise HTTPException(status_code=400, detail="缺少收藏项目 id")

    exists = any(item.get("id") == item_id for item in user_state["favorites"])
    if not exists:
        user_state["favorites"].append(json.loads(json.dumps(data)))
        sync_user_counts()

    return ApiResponse(data={"success": True, "message": "收藏成功"})


@app.delete("/user/favorites/{item_id}")
async def remove_favorite(item_id: str):
    before = len(user_state["favorites"])
    user_state["favorites"] = [item for item in user_state["favorites"] if item.get("id") != item_id]
    if len(user_state["favorites"]) == before:
        raise HTTPException(status_code=404, detail="收藏不存在")

    sync_user_counts()
    return ApiResponse(data={"success": True, "message": "取消收藏成功"})


@app.get("/user/history")
async def get_user_history():
    sync_user_counts()
    return ApiResponse(data={
        "list": user_state["history"],
        "total": len(user_state["history"])
    })


@app.post("/admin/login")
async def admin_login(data: Dict[str, Any]):
    username = data.get("username")
    password = data.get("password")

    if admin_credentials.get(username) != password:
        raise HTTPException(status_code=401, detail="管理员账号或密码错误")

    token = f"admin-{uuid.uuid4().hex}"
    admin_tokens.add(token)
    return ApiResponse(data={
        "token": token,
        "username": username
    })


@app.get("/admin/members")
async def get_admin_members(authorization: Optional[str] = Header(None)):
    token = parse_bearer_token(authorization)
    if token not in admin_tokens:
        raise HTTPException(status_code=401, detail="未登录或登录已过期")

    return ApiResponse(data={
        "members": user_state["members"],
        "total": len(user_state["members"])
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
