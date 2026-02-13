"""
Health API - 健康检查接口
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """服务健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Customer Service Bot",
        "version": "1.0.0"
    }


@router.get("/ready")
async def readiness_check():
    """就绪检查"""
    return {
        "ready": True,
        "timestamp": datetime.now().isoformat()
    }
