from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from app.database import get_db, get_redis, mongodb_connected, redis_connected

# 创建FastAPI应用
app = FastAPI(
    title="酱酒研学平台API",
    description="酱酒研学平台后端API接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存数据存储（当MongoDB不可用时使用）
memory_data = {
    "knowledge": [],
    "production": [],
    "wineries": [],
    "news": []
}

# 如果MongoDB不可用，从JSON文件加载模拟数据
if not mongodb_connected:
    import os
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    for name in memory_data:
        json_path = os.path.join(data_dir, f"{name}.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                memory_data[name] = json.load(f)
            print(f"✓ 从 {json_path} 加载了 {len(memory_data[name])} 条 {name} 数据")


def get_collection(name):
    """获取集合，优先使用MongoDB，否则使用内存存储"""
    if mongodb_connected and get_db() is not None:
        return get_db()[name]
    return None


def find_documents(collection_name, query=None, limit=100, skip=0):
    """查询文档"""
    if query is None:
        query = {}
    
    collection = get_collection(collection_name)
    if collection is not None:
        cursor = collection.find(query).skip(skip).limit(limit)
        # 转换ObjectId为字符串
        result = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            result.append(doc)
        return result
    else:
        # 内存模式
        data = memory_data[collection_name]
        if query:
            # 简单过滤
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
    """统计文档数量"""
    if query is None:
        query = {}
    
    collection = get_collection(collection_name)
    if collection is not None:
        return collection.count_documents(query)
    else:
        # 内存模式：直接统计匹配的文档数
        items = memory_data.get(collection_name, [])
        if not query or query == {}:
            return len(items)
        return sum(1 for item in items if all(item.get(k) == v for k, v in query.items()))


def find_one(collection_name, query):
    """查询单个文档"""
    results = find_documents(collection_name, query, limit=1)
    return results[0] if results else None


# 响应模型
class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


@app.get("/")
async def root():
    """根路径"""
    return ApiResponse(data={
        "service": "酱酒研学平台API",
        "version": "1.0.0",
        "mongodb": "connected" if mongodb_connected else "memory_mode",
        "redis": "connected" if redis_connected else "memory_mode"
    })


@app.get("/health")
async def health_check():
    """健康检查"""
    return ApiResponse(data={
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.get("/dashboard")
async def get_dashboard():
    """首页数据看板"""
    try:
        knowledge_count = count_documents("knowledge")
        production_count = count_documents("production")
        wineries_count = count_documents("wineries")
        news_count = count_documents("news")
        
        # 获取最新资讯
        latest_news = find_documents("news", limit=5)
        # 获取热门酒厂
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
    """获取知识库列表"""
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
    """获取知识库分类"""
    categories = [
        {"id": "culture", "name": "酱酒文化", "count": 0},
        {"id": "craft", "name": "酿造工艺", "count": 0},
        {"id": "tasting", "name": "品鉴指南", "count": 0},
        {"id": "production", "name": "产区介绍", "count": 0}
    ]
    
    # 统计各类别数量
    for cat in categories:
        cat["count"] = count_documents("knowledge", {"category": cat["id"]})
    
    return ApiResponse(data=categories)


@app.get("/knowledge/{item_id}")
async def get_knowledge_detail(item_id: str):
    """获取知识库详情"""
    item = find_one("knowledge", {"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="文章不存在")
    return ApiResponse(data=item)


@app.get("/production")
async def get_production_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000)
):
    """获取产区列表"""
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
    """获取产区统计数据"""
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
    """获取产区详情"""
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
    """获取酒厂名录"""
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
    """获取酒厂详情"""
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
    """获取资讯列表"""
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
    """获取资讯详情"""
    item = find_one("news", {"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="资讯不存在")
    return ApiResponse(data=item)


@app.get("/search")
async def search(keyword: str = Query(..., min_length=1)):
    """全站搜索"""
    try:
        query = {"$regex": keyword, "$options": "i"}
        
        # 搜索知识库
        knowledge_results = find_documents("knowledge", {"title": query}, limit=10)
        
        # 搜索酒厂
        wineries_results = find_documents("wineries", {"name": query}, limit=10)
        
        # 搜索产区
        production_results = find_documents("production", {"name": query}, limit=10)
        
        # 搜索资讯
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
    """获取热门搜索"""
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
    """获取用户信息（模拟）"""
    return ApiResponse(data={
        "id": "user_001",
        "nickname": "酱酒爱好者",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=jiangjiu",
        "favorite_count": 12,
        "history_count": 36
    })


@app.get("/user/favorites")
async def get_user_favorites():
    """获取收藏列表（模拟）"""
    # 返回空列表，模拟用户暂无收藏
    return ApiResponse(data={"list": [], "total": 0})


@app.post("/user/favorites")
async def add_favorite(data: Dict[str, Any]):
    """添加收藏（模拟）"""
    return ApiResponse(data={"success": True, "message": "收藏成功"})


@app.delete("/user/favorites/{item_id}")
async def remove_favorite(item_id: str):
    """取消收藏（模拟）"""
    return ApiResponse(data={"success": True, "message": "取消收藏成功"})


@app.get("/user/history")
async def get_user_history():
    """获取浏览历史（模拟）"""
    return ApiResponse(data={"list": [], "total": 0})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
