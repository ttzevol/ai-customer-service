"""
Data Models - 数据模型定义
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """消息角色"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """对话消息"""
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None


class DocumentType(str, Enum):
    """文档类型"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "md"
    UNKNOWN = "unknown"


class DocumentStatus(str, Enum):
    """文档处理状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class Document(BaseModel):
    """知识库文档"""
    id: str
    filename: str
    file_type: DocumentType
    file_size: int
    status: DocumentStatus
    chunk_count: int = 0
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = {}


class DocumentCreate(BaseModel):
    """创建文档请求"""
    filename: str
    file_type: DocumentType
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """对话请求"""
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    max_history: int = 10


class ChatResponse(BaseModel):
    """对话响应"""
    response: str
    session_id: str
    sources: List[Dict[str, Any]] = []
    confidence: float = 0.0
    timestamp: datetime


class SearchResult(BaseModel):
    """搜索结果"""
    document_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}


class User(BaseModel):
    """用户"""
    id: str
    username: str
    email: Optional[str] = None
    api_key: Optional[str] = None
    plan: str = "free"
    usage_count: int = 0
    created_at: datetime


class UsageStats(BaseModel):
    """使用统计"""
    user_id: str
    total_requests: int
    total_tokens: int
    successful_requests: int
    failed_requests: int
    period_start: datetime
    period_end: datetime
