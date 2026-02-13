"""
API Tests - API 接口测试
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthAPI:
    """健康检查接口测试"""
    
    def test_health_check(self):
        """测试健康检查"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_readiness_check(self):
        """测试就绪检查"""
        response = client.get("/api/v1/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] == True


class TestChatAPI:
    """对话接口测试"""
    
    def test_chat_without_session(self):
        """测试无会话ID的对话"""
        response = client.post(
            "/api/v1/chat",
            json={"message": "你好"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert "timestamp" in data
    
    def test_chat_with_session(self):
        """测试有会话ID的对话"""
        session_id = "test-session-001"
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "第二个问题",
                "session_id": session_id
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == session_id
    
    def test_get_history(self):
        """测试获取对话历史"""
        response = client.get("/api/v1/history/test-session-001")
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
    
    def test_clear_history(self):
        """测试清除对话历史"""
        response = client.delete("/api/v1/history/test-session-001")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cleared"
    
    def test_chat_empty_message(self):
        """测试空消息"""
        response = client.post(
            "/api/v1/chat",
            json={"message": ""}
        )
        # 空消息应该被处理
        assert response.status_code in [200, 422]


class TestRoot:
    """根路径测试"""
    
    def test_root(self):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "AI Customer Service Bot"
        assert data["version"] == "1.0.0"
