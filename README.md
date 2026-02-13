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

## 📦 Pricing

| Plan | Price | Includes |
|------|-------|----------|
| Free | $0 | 100 calls/month |
| Pro | $99/month | Unlimited + Support |
| Enterprise | $299/month | Unlimited + Custom |

## 📄 License

MIT License - Free for commercial use!

## ⭐ Star Us!

If this project helps you, please give us a star! 🌟

```bash
gh repo star ttzevol/ai-customer-service
```

---

<p align="center">
  Made with ❤️
</p>
