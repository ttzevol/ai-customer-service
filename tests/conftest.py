"""
Test Configuration - 测试配置
"""

import pytest
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 测试配置
TEST_CONFIG = {
    "OPENAI_API_KEY": "test-key",
    "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
    "MILVUS_HOST": "localhost",
    "MILVUS_PORT": "19530",
}


@pytest.fixture(scope="session")
def project_root():
    """项目根目录"""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def app_dir(project_root):
    """应用目录"""
    return project_root / "ai-customer-service"


@pytest.fixture
def mock_openai_key():
    """模拟OpenAI API Key"""
    os.environ["OPENAI_API_KEY"] = "sk-test-key"
    yield
    os.environ.pop("OPENAI_API_KEY", None)
