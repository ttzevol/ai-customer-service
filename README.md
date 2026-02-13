# 🤖 AI Customer Service Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![GitHub Stars](https://img.shields.io/github/stars/ttzevol/ai-customer-service?style=social)](https://github.com/ttzevol/ai-customer-service/stargazers)

> 基于 LangGraph + RAG 的企业级智能客服机器人，支持知识库管理和多轮对话 🚀

## ✨ 特性

- 🧠 **智能问答** - 基于 RAG 的向量检索，精准匹配知识库
- 🔄 **多轮对话** - LangGraph 工作流编排，上下文理解能力强
- 📚 **知识库管理** - 支持 PDF/Word/TXT 文档自动解析
- ⚡ **高性能** - FastAPI + 异步处理，响应快速
- 🐳 **一键部署** - Docker Compose 容器化，开箱即用
- 🔌 **完整 API** - RESTful 接口，易于集成

## 🛠 技术栈

<div align="center">

| 类别 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| AI 框架 | LangChain + LangGraph |
| 向量数据库 | Milvus / Chroma |
| LLM | OpenAI GPT-4 / Claude / Gemini |
| 数据库 | SQLite / PostgreSQL |
| 部署 | Docker / Docker Compose |

</div>

## 📦 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/ttzevol/ai-customer-service.git
cd ai-customer-service
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

### 4. 启动服务

```bash
# 启动向量数据库（可选）
docker-compose up -d milvus

# 启动应用
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

## 🐳 Docker 部署

```bash
# 一键启动所有服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📡 API 使用示例

### 发送对话消息

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你们的定价是怎样的？", "session_id": "user_123"}'
```

### 上传知识库

```bash
curl -X POST "http://localhost:8000/api/v1/knowledge/upload" \
  -F "file=@manual.pdf"
```

## 📁 项目结构

```
ai-customer-service/
├── app/
│   ├── api/              # FastAPI 路由
│   │   ├── chat.py      # 对话接口
│   │   ├── knowledge.py  # 知识库接口
│   │   └── health.py     # 健康检查
│   ├── core/            # 配置管理
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑
│   │   ├── rag_service.py    # RAG 检索服务
│   │   ├── llm_service.py    # LLM 调用封装
│   │   └── chat_service.py   # 对话服务
│   ├── graph/           # LangGraph 工作流
│   └── knowledge/       # 知识库管理
├── tests/               # 测试用例
├── scripts/             # 部署脚本
├── docs/                # 文档
├── docker-compose.yml   # Docker 编排
├── requirements.txt     # Python 依赖
└── README.md            # 项目说明
```

## 💰 商业模式

| 方案 | 价格 | 包含 |
|------|------|------|
| Free | ¥0 | 100次/月，体验版 |
| Pro | ¥99/月 | 无限调用，基础支持 |
| Enterprise | ¥299/月 | 无限调用，定制服务 |

## 📈 路线图

- [x] MVP 版本发布
- [ ] LangGraph 工作流集成
- [ ] 多轮对话支持
- [ ] 用户管理系统
- [ ] Web 管理后台
- [ ] 定价页面
- [ ] 生产环境部署

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⭐ 如果对你有帮助，请 star 支持！

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=ttzevol/ai-customer-service&type=Date)](https://star-history.com/#ttzevol/ai-customer-service&Date)

</div>

## 📞 联系

- GitHub Issues: [https://github.com/ttzevol/ai-customer-service/issues](https://github.com/ttzevol/ai-customer-service/issues)
- 作者: [@ttzevol](https://github.com/ttzevol)

---

<p align="center">
  用 ❤️ 构建
</p>
