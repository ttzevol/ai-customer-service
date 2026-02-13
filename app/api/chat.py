"""
Chat API - 对话接口

提供智能对话功能，基于 RAG + LLM 实现。
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.services.chat_service import ChatService, get_chat_service

router = APIRouter()

# 全局 ChatService 实例
_chat_service: Optional[ChatService] = None


def get_chat_service_instance() -> ChatService:
    """获取 ChatService 实例"""
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service


class ChatMessage(BaseModel):
    """对话消息请求"""
    message: str = Field(..., min_length=1, max_length=10000, description="用户消息")
    session_id: Optional[str] = Field(None, max_length=64, description="会话ID")
    user_id: Optional[str] = Field(None, max_length=64, description="用户ID")
    use_rag: bool = Field(True, description="是否使用知识库检索")
    stream: bool = Field(False, description="是否流式输出")


class ChatResponse(BaseModel):
    """对话响应"""
    response: str = Field(..., description="AI回复内容")
    session_id: str = Field(..., description="会话ID")
    sources: List[dict] = Field(default_factory=list, description="参考来源")
    confidence: float = Field(0.0, ge=0, le=1, description="回答置信度")
    timestamp: datetime = Field(..., description="响应时间")


class ChatHistoryResponse(BaseModel):
    """对话历史响应"""
    session_id: str = Field(...)
    messages: List[dict] = Field(..., description="消息列表")
    message_count: int = Field(..., description="消息数量")
    created_at: Optional[str] = Field(None, description="创建时间")
    updated_at: Optional[str] = Field(None, description="更新时间")


class SourceItem(BaseModel):
    """来源信息"""
    filename: str
    score: float
    content_preview: str = ""


class SourcesResponse(BaseModel):
    """知识库搜索结果"""
    query: str
    results: List[SourceItem]
    total: int


# 模拟的对话存储（备用，保持向后兼容）
chat_sessions = {}


@router.post("/chat", response_model=ChatResponse)
async def send_message(
    request: ChatMessage,
    chat_service: ChatService = Depends(get_chat_service_instance)
):
    """
    发送对话消息，获取AI回复

    - message: 用户消息（必需）
    - session_id: 会话ID（可选，自动生成）
    - user_id: 用户ID（可选）
    - use_rag: 是否使用知识库检索（默认True）
    - stream: 是否流式输出（默认False）

    **功能说明：**
    - 自动检索知识库相关内容
    - 支持多轮对话记忆
    - 返回参考来源和置信度
    """
    try:
        # 调用对话服务
        result = chat_service.chat(
            message=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            use_rag=request.use_rag,
            stream=request.stream
        )

        # 兼容旧格式：同时保存到模拟存储
        session_id = result["session_id"]
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                "messages": [],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

        # 保存对话历史
        chat_sessions[session_id]["messages"].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })
        chat_sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": result["response"],
            "timestamp": datetime.now().isoformat()
        })
        chat_sessions[session_id]["updated_at"] = datetime.now()

        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            sources=request.use_rag and result.get("sources", []) or [],
            confidence=result.get("confidence", 0.0),
            timestamp=datetime.now()
        )

    except Exception as e:
        logging.error(f"对话处理失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service_instance)
):
    """
    获取对话历史

    - session_id: 会话ID
    """
    # 尝试从真实服务获取
    history = chat_service.get_history(session_id)

    if not history:
        # 降级到模拟存储
        if session_id not in chat_sessions:
            raise HTTPException(status_code=404, detail="会话不存在")
        history = chat_sessions[session_id]["messages"]

    return ChatHistoryResponse(
        session_id=session_id,
        messages=history,
        message_count=len(history),
        created_at=history[0]["timestamp"] if history else None,
        updated_at=history[-1]["timestamp"] if history else None
    )


@router.delete("/history/{session_id}")
async def clear_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service_instance)
):
    """
    清除对话历史
    """
    # 清除真实服务历史
    chat_service.clear_history(session_id)

    # 清除模拟存储
    if session_id in chat_sessions:
        del chat_sessions[session_id]

    return {"status": "cleared", "session_id": session_id}


@router.get("/sessions/count")
async def get_session_count(
    chat_service: ChatService = Depends(get_chat_service_instance)
):
    """
    获取当前会话数量
    """
    return {
        "count": chat_service.get_session_count()
    }
