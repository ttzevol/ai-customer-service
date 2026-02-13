"""
Database Models - 数据库模型
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class DocumentModel(Base):
    """知识库文档模型"""
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)
    file_size = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")
    chunk_count = Column(Integer, default=0)
    content_hash = Column(String(64))
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatSessionModel(Base):
    """对话会话模型"""
    __tablename__ = "chat_sessions"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    title = Column(String(255))
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatMessageModel(Base):
    """对话消息模型"""
    __tablename__ = "chat_messages"
    
    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, default=0)
    latency_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserModel(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    api_key = Column(String(64), unique=True)
    plan = Column(String(20), default="free")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UsageLogModel(Base):
    """使用日志模型"""
    __tablename__ = "usage_logs"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    request_type = Column(String(50))
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables(engine):
    """创建所有表"""
    Base.metadata.create_all(engine)


def drop_tables(engine):
    """删除所有表"""
    Base.metadata.drop_all(engine)
