# ⚙️ 配置完整指南

本文档详细介绍所有配置选项。

## 📋 目录

- [基础配置](#基础配置)
- [数据库配置](#数据库配置)
- [AI 模型配置](#ai-模型配置)
- [向量数据库配置](#向量数据库配置)
- [缓存配置](#缓存配置)
- [日志配置](#日志配置)
- [高级配置](#高级配置)

---

## 🔧 基础配置

### 必需配置

| 环境变量 | 默认值 | 描述 |
|---------|--------|------|
| `OPENAI_API_KEY` | - | OpenAI API Key（必需） |
| `ENVIRONMENT` | `development` | 运行环境：`development` / `production` |
| `DEBUG` | `false` | 调试模式开关 |
| `SECRET_KEY` | - | JWT 签名密钥 |
| `ALGORITHM` | `HS256` | JWT 算法 |

### 可选配置

| 环境变量 | 默认值 | 描述 |
|---------|--------|------|
| `HOST` | `0.0.0.0` | 服务监听地址 |
| `PORT` | `8000` | 服务监听端口 |
| `WORKERS` | `1` | Uvicorn worker 数量 |
| `LOG_LEVEL` | `INFO` | 日志级别：`DEBUG` / `INFO` / `WARNING` / `ERROR` |

### 示例 `.env`

```bash
# 必需配置
OPENAI_API_KEY=sk-your-api-key-here
SECRET_KEY=your-secret-key-at-least-32-chars

# 环境配置
ENVIRONMENT=production
DEBUG=false

# 服务配置
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=INFO
```

---

## 🗄️ 数据库配置

### PostgreSQL（推荐）

```bash
# 方式1：直接连接
DATABASE_URL=postgresql://username:password@host:5432/database_name

# 方式2：Docker Compose 环境变量
POSTGRES_DB=ai_customer_service
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# SQLAlchemy URL（自动构建）
# postgresql://admin:your_password@db:5432/ai_customer_service
```

### SQLite（开发环境）

```bash
DATABASE_URL=sqlite:///./data/ai_customer_service.db
```

### 配置选项

| 环境变量 | 默认值 | 描述 |
|---------|--------|------|
| `DATABASE_POOL_SIZE` | `5` | 连接池大小 |
| `DATABASE_MAX_OVERFLOW` | `10` | 连接池最大溢出 |
| `DATABASE_POOL_TIMEOUT` | `30` | 连接超时（秒） |
| `DATABASE_POOL_RECYCLE` | `1800` | 连接回收时间（秒） |

---

## 🤖 AI 模型配置

### OpenAI（默认）

```bash
# 必需
OPENAI_API_KEY=sk-your-key

# 可选（覆盖默认值）
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
OPENAI_TIMEOUT=60
OPENAI_MAX_RETRIES=3
```

### Anthropic Claude

```bash
# 切换模型
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=2000
```

### Google Gemini

```bash
AI_PROVIDER=google
GOOGLE_API_KEY=your-gemini-key
GOOGLE_MODEL=gemini-pro
```

### 多模型配置

```python
# config.py - 多模型支持
AI_CONFIG = {
    "default": "openai",
    "models": {
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            "temperature": float(os.getenv("OPENAI_TEMPERATURE", 0.7)),
        },
        "anthropic": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
        },
        "google": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "model": os.getenv("GOOGLE_MODEL", "gemini-pro"),
        }
    }
}
```

---

## 🧮 向量数据库配置

### Milvus（推荐）

```bash
# 必需
MILVUS_HOST=localhost
MILVUS_PORT=19530

# 可选
MILVUS_DB_NAME=default
MILVUS_COLLECTION=knowledge_base
MILVUS_INDEX_TYPE=HNSW
MILVUS_METRIC_TYPE=COSINE
MILVUS_VECTOR_DIM=1536
```

### Milvus Docker

```yaml
# docker-compose.yml
services:
  milvus-standalone:
    image: milvusdb/milvus:latest
    ports:
      - "19530:19530"
    environment:
      ETCD_USE_EMBED: true
      STORAGE_USE_EMBED: true
```

### Chroma（轻量级）

```bash
# 使用 Chroma
VECTOR_DB=chroma
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_PERSIST_DIR=./data/chroma
```

---

## 💾 缓存配置

### Redis

```bash
# 启用 Redis
USE_REDIS=true
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 连接选项
REDIS_MAX_CONNECTIONS=50
REDIS_TIMEOUT=5
REDIS_SOCKET_TIMEOUT=5
```

### 缓存策略

```python
# config.py - 缓存配置
CACHE_CONFIG = {
    "enabled": os.getenv("USE_REDIS", "false").lower() == "true",
    "default_ttl": 3600,  # 1小时
    "session_ttl": 86400,  # 24小时
    "knowledge_ttl": None,  # 知识库不缓存
    "llm_response_ttl": None,  # LLM 响应不缓存
}
```

---

## 📝 日志配置

### 日志级别

| 级别 | 描述 | 使用场景 |
|------|------|---------|
| `DEBUG` | 详细调试信息 | 开发环境排错 |
| `INFO` | 一般信息 | 正常运行时 |
| `WARNING` | 警告信息 | 需要注意但不严重 |
| `ERROR` | 错误信息 | 系统故障 |

### JSON 日志（生产环境）

```bash
LOG_FORMAT=json
LOG_FILE=/var/log/ai-customer-service/app.log
LOG_MAX_SIZE=100MB
LOG_BACKUP_COUNT=5
```

### 结构化日志示例

```json
{
  "timestamp": "2025-02-12T10:30:00Z",
  "level": "INFO",
  "message": "收到对话请求",
  "request_id": "req_abc123",
  "session_id": "sess_xyz789",
  "response_time_ms": 245,
  "user_id": "user_001"
}
```

---

## 🔒 安全配置

### CORS 跨域

```bash
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
CORS_ALLOW_CREDENTIALS=true
```

### 速率限制

```bash
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # 60秒
```

### IP 白名单

```bash
# 只允许特定 IP 访问
ALLOWED_IPS=192.168.1.1,10.0.0.0/8
```

---

## 📊 性能配置

### 并发处理

```bash
# Uvicorn workers
WORKERS=4

# 异步配置
UVICORN_ASYNC=true
UVICORN_LOOP=uvloop

# 数据库连接池
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

### 内存优化

```bash
# Python 垃圾回收
PYTHONOPTIMIZE=2
PYTHONGC=1000

# Milvus 内存
MILVUS_USE_GPU=false  # 设为 true 可用 GPU 加速
MILVUS_RESOURCE_MODE=automatic
```

---

## 🌍 国际化配置

### 支持语言

```bash
# 默认语言
DEFAULT_LANGUAGE=zh-CN

# 支持的语言列表
SUPPORTED_LANGUAGES=zh-CN,en-US,ja-JP

# 自动检测
AUTO_DETECT_LANGUAGE=true
```

---

## 📦 完整配置示例

### 开发环境 `.env`

```bash
# ========================================
# AI Customer Service Bot - 开发环境配置
# ========================================

# 必需配置
OPENAI_API_KEY=sk-your-openai-key
SECRET_KEY=dev-secret-key-at-least-32-characters

# 环境配置
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# 服务配置
HOST=0.0.0.0
PORT=8000
WORKERS=1

# 数据库（SQLite）
DATABASE_URL=sqlite:///./data/dev.db

# Redis（可选）
USE_REDIS=false

# Milvus（本地 Docker）
MILVUS_HOST=localhost
MILVUS_PORT=19530

# AI 模型
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# CORS
CORS_ORIGINS=["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS=true

# 速率限制
RATE_LIMIT_ENABLED=false
```

### 生产环境 `.env.production`

```bash
# ========================================
# AI Customer Service Bot - 生产环境配置
# ========================================

# 必需配置
OPENAI_API_KEY=sk-prod-openai-key
SECRET_KEY=prod-secret-key-at-least-32-chars-change-this

# 环境配置
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/ai-customer-service/app.log

# 服务配置
HOST=0.0.0.0
PORT=8000
WORKERS=4

# 数据库（PostgreSQL）
POSTGRES_DB=ai_customer_service
POSTGRES_USER=admin
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis
USE_REDIS=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_MAX_CONNECTIONS=50

# Milvus
MILVUS_HOST=milvus-standalone
MILVUS_PORT=19530
MILVUS_INDEX_TYPE=HNSW
MILVUS_METRIC_TYPE=COSINE

# AI 模型
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
OPENAI_TIMEOUT=60
OPENAI_MAX_RETRIES=3

# CORS
CORS_ORIGINS=["https://yourdomain.com"]
CORS_ALLOW_CREDENTIALS=true

# 速率限制
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# 安全
ALLOWED_IPS=
```

---

## 🔧 配置验证

启动前验证配置：

```python
# scripts/validate_config.py

import os
from pydantic import BaseModel, Field

class Config(BaseModel):
    OPENAI_API_KEY: str = Field(..., min_length=10)
    SECRET_KEY: str = Field(..., min_length=32)
    ENVIRONMENT: str = Field(default="development")
    DATABASE_URL: str

def validate():
    required = ["OPENAI_API_KEY", "SECRET_KEY", "DATABASE_URL"]
    for key in required:
        if not os.getenv(key):
            raise ValueError(f"缺少必需配置: {key}")
    print("✅ 配置验证通过！")

if __name__ == "__main__":
    validate()
```

---

## 📚 相关文档

- [部署指南](DEPLOYMENT.md)
- [架构设计](ARCHITECTURE.md)
- [API 文档](API.md)
