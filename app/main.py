"""
AI Customer Service Bot - Main Application
基于FastAPI的智能客服机器人API服务
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import chat, knowledge, health

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("🚀 AI Customer Service Bot 启动中...")
    logger.info(f"📡 API文档: http://{settings.APP_HOST}:{settings.APP_PORT}/docs")
    logger.info(f"🔧 调试模式: {settings.DEBUG}")
    
    yield
    
    # 关闭时
    logger.info("👋 AI Customer Service Bot 关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title="AI Customer Service Bot",
    description="基于LangGraph + RAG的智能客服机器人API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])
app.include_router(chat.router, prefix="/api/v1", tags=["对话"])
app.include_router(knowledge.router, prefix="/api/v1", tags=["知识库"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI Customer Service Bot",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
