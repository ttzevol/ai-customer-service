"""
Database Initialization - 数据库初始化
"""

import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.database import Base, create_tables

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def init_database():
    """初始化数据库"""
    # 确保data目录存在
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # 创建数据库URL
    db_url = settings.DATABASE_URL
    
    # 创建引擎
    engine = create_async_engine(db_url, echo=settings.DEBUG)
    
    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 关闭引擎
    await engine.dispose()
    
    print("✅ 数据库初始化完成！")
    print(f"📁 数据库文件: {settings.DATABASE_URL}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_database())
