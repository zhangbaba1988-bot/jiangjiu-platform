from pymongo import MongoClient
import redis
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "jiangjiu_research"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()

# MongoDB连接
mongo_client: Optional[MongoClient] = None
db = None


def init_mongodb():
    """初始化MongoDB连接"""
    global mongo_client, db
    try:
        mongo_client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
        # 测试连接
        mongo_client.admin.command('ping')
        db = mongo_client[settings.MONGODB_DB_NAME]
        print("✓ MongoDB连接成功")
        return True
    except Exception as e:
        print(f"✗ MongoDB连接失败: {e}")
        print("  使用内存模式运行...")
        return False


# Redis连接
redis_client: Optional[redis.Redis] = None


def init_redis():
    """初始化Redis连接"""
    global redis_client
    try:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_client.ping()
        print("✓ Redis连接成功")
        return True
    except Exception as e:
        print(f"✗ Redis连接失败: {e}")
        print("  使用内存模式运行...")
        return False


def get_db():
    """获取数据库实例"""
    return db


def get_redis():
    """获取Redis实例"""
    return redis_client


# 初始化连接
mongodb_connected = init_mongodb()
redis_connected = init_redis()
