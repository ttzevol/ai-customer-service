# AI智能客服机器人 - 使用指南

## 📋 目录

1. [快速开始](#快速开始)
2. [配置说明](#配置说明)
3. [API使用](#api使用)
4. [部署到生产环境](#部署到生产环境)
5. [常见问题](#常见问题)

---

## 🚀 快速开始

### 1. 克隆项目

```bash
cd /Users/wubowen/.openclaw/workspace/projects
git clone <repo-url> ai-customer-service
cd ai-customer-service
```

### 2. 配置环境

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑配置文件
nano .env
```

编辑 `.env` 文件：

```env
# OpenAI API Key（必需）
OPENAI_API_KEY=sk-your-api-key-here

# 数据库（使用SQLite）
DATABASE_URL=sqlite+aiosqlite:///./data/app.db

# Milvus配置（可选，使用内存模式）
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### 3. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装Python依赖
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
python scripts/init_db.py
```

### 5. 启动服务

```bash
# 开发模式
python scripts/run_dev.py

# 或直接使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 测试

打开浏览器访问：

- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

---

## ⚙️ 配置说明

### 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API Key |
| `OPENAI_MODEL` | ❌ | gpt-4-turbo-preview | 使用的模型 |
| `DATABASE_URL` | ❌ | SQLite | 数据库连接字符串 |
| `MILVUS_HOST` | ❌ | localhost | Milvus服务器地址 |
| `MILVUS_PORT` | ❌ | 19530 | Milvus端口 |
| `DEBUG` | ❌ | false | 调试模式 |
| `LOG_LEVEL` | ❌ | INFO | 日志级别 |

### 更换LLM提供商

#### OpenAI（默认）

```env
OPENAI_API_KEY=sk-your-key
```

#### Anthropic Claude

```env
ANTHROPIC_API_KEY=your-claude-key
ANTHROPIC_MODEL=claude-3-opus-20240229
```

#### 本地模型（Ollama）

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

---

## 📡 API使用

### 1. 发送对话请求

**POST** `/api/v1/chat`

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你们的服务有什么特点？"}'
```

**请求体：**

```json
{
  "message": "你们的收费标准是什么？",
  "session_id": "user-123",
  "user_id": "user-123"
}
```

**响应：**

```json
{
  "response": "我们提供三种套餐...",
  "session_id": "user-123",
  "sources": [
    {
      "document_id": "doc-001",
      "filename": "pricing.md",
      "score": 0.95
    }
  ],
  "confidence": 0.92,
  "timestamp": "2026-02-12T19:00:00"
}
```

### 2. 上传知识库文档

**POST** `/api/v1/knowledge/upload`

```bash
curl -X POST "http://localhost:8000/api/v1/knowledge/upload" \
  -F "file=@./docs/faq.pdf"
```

**响应：**

```json
{
  "id": "doc-001",
  "filename": "faq.pdf",
  "message": "文档上传成功，等待处理",
  "status": "pending"
}
```

### 3. 列出知识库文档

**GET** `/api/v1/knowledge/list`

```bash
curl "http://localhost:8000/api/v1/knowledge/list"
```

**响应：**

```json
{
  "documents": [
    {
      "id": "doc-001",
      "filename": "faq.pdf",
      "file_type": "pdf",
      "size": 1024000,
      "chunks": 150,
      "status": "indexed"
    }
  ],
  "total": 1
}
```

### 4. 获取对话历史

**GET** `/api/v1/history/{session_id}`

```bash
curl "http://localhost:8000/api/v1/history/user-123"
```

---

## 🐳 部署到生产环境

### Docker部署（推荐）

```bash
# 1. 配置生产环境变量
cp .env.example .env
# 编辑 .env 文件

# 2. 确保数据目录存在
mkdir -p data/milvus data/chroma

# 3. 部署
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Docker Compose服务

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 手动部署

```bash
# 1. 安装Python 3.11
# 2. 安装Milvus（参考：https://milvus.io/docs/install-overview.md）
# 3. 配置Nginx反向代理
# 4. 使用systemd管理进程
```

### 生产环境配置

#### Nginx配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Systemd服务

```ini
# /etc/systemd/system/ai-customer.service
[Unit]
Description=AI Customer Service Bot
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/ai-customer-service
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## ❓ 常见问题

### Q1: 启动报错 "OPENAI_API_KEY not set"

**解决：** 确保 `.env` 文件中设置了有效的 API Key。

### Q2: Milvus连接失败

**解决：** 
- 使用 Docker 启动 Milvus：`docker-compose up -d milvus`
- 或使用内存模式（开发环境）

### Q3: 如何添加新的知识库？

**解决：** 使用 `/api/v1/knowledge/upload` 接口上传文档，或直接放入 `data/documents` 目录。

### Q4: 如何切换到其他LLM？

**解决：** 修改 `.env` 文件中的配置，支持 OpenAI、Anthropic、本地模型等。

### Q5: 如何监控服务状态？

**解决：** 
- 健康检查：`http://localhost:8000/health`
- 查看日志：`docker-compose logs -f`
- 集成 Prometheus + Grafana

---

## 📚 更多资源

- [API文档](http://localhost:8000/docs)
- [LangChain文档](https://python.langchain.com/)
- [LangGraph文档](https://langchain-ai.github.io/langgraph/)
- [Milvus文档](https://milvus.io/docs/overview.md)

---

## 📞 支持

如有问题，请提交 Issue 或联系开发团队。
