# 🤖 AI Customer Service Bot

> **🇨🇳 中文介绍请查看 [README_CN.md](./README_CN.md)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![GitHub Stars](https://img.shields.io/github/stars/ttzevol/ai-customer-service?style=social)](https://github.com/ttzevol/ai-customer-service/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ttzevol/ai-customer-service?style=social)](https://github.com/ttzevol/ai-customer-service/network)
[![Contributors](https://img.shields.io/github/contributors/ttzevol/ai-customer-service)](https://github.com/ttzevol/ai-customer-service/graphs/contributors)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/ttzevol/ai-customer-service/ci.yml)](https://github.com/ttzevol/ai-customer-service/actions)
[![Coverage](https://img.shields.io/codecov/c/github/ttzevol/ai-customer-service)](https://codecov.io/gh/ttzevol/ai-customer-service)

> Enterprise-grade AI Customer Service Bot with RAG and LangGraph 🚀

## ✨ Features

- 🧠 **Smart Q&A** - RAG-based vector retrieval with knowledge base
- 🔄 **Multi-turn Dialogue** - LangGraph workflow orchestration
- 📚 **Knowledge Management** - PDF/Word/TXT document processing
- ⚡ **High Performance** - FastAPI with async support
- 🐳 **Docker Ready** - Containerized deployment
- 🔌 **Complete API** - RESTful interfaces for easy integration

## 🛠 Tech Stack

<div align="center">

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| AI Framework | LangChain + LangGraph |
| Vector DB | Milvus / Chroma |
| LLM | OpenAI GPT-4 / Claude / Gemini |
| Deployment | Docker / Docker Compose |

</div>

## 🚀 Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/ttzevol/ai-customer-service.git
cd ai-customer-service
docker-compose up -d --build
```

### Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for API documentation.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README_CN.md](./README_CN.md) | 中文项目介绍 |
| [docs/API.md](./docs/API.md) | API 接口文档 |
| [docs/USER_GUIDE.md](./docs/USER_GUIDE.md) | 使用指南 |
| [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) | 生产环境部署 |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | 系统架构设计 |
| [docs/CONFIGURATION.md](./docs/CONFIGURATION.md) | 配置完整指南 |
| [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) | 贡献指南 |
| [docs/SOCIAL_PROMOTION.md](./docs/SOCIAL_PROMOTION.md) | 社交媒体推广文案 |

## 🏗️ Project Structure

```
ai-customer-service/
├── app/                      # 核心应用代码
│   ├── api/                  # FastAPI 路由
│   │   ├── chat.py          # 对话接口
│   │   ├── knowledge.py     # 知识库接口
│   │   └── health.py        # 健康检查
│   ├── core/                # 配置管理
│   ├── models/              # 数据模型
│   ├── services/            # 业务逻辑
│   │   ├── rag_service.py   # RAG 检索服务
│   │   ├── llm_service.py   # LLM 调用封装
│   │   └── chat_service.py  # 对话服务
│   ├── graph/               # LangGraph 工作流
│   └── knowledge/           # 知识库管理
├── tests/                    # 测试用例
├── scripts/                  # 部署脚本
├── docs/                     # 完整文档
├── docker-compose.yml        # Docker 编排
├── requirements.txt          # Python 依赖
└── README.md                 # 项目说明
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for details.

---

<p align="center">
  Made with ❤️
</p>
