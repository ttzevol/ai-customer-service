# 🤖 AI Customer Service Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![GitHub Stars](https://img.shields.io/github/stars/ttzevol/ai-customer-service?style=social)](https://github.com/ttzevol/ai-customer-service/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ttzevol/ai-customer-service?style=social)](https://github.com/ttzevol/ai-customer-service/network)
[![Contributors](https://img.shields.io/github/contributors/ttzevol/ai-customer-service)](https://github.com/ttzevol/ai-customer-service/graphs/contributors)

> 🇨🇳 基于 LangGraph + RAG 的企业级智能客服机器人，支持知识库管理和多轮对话 🚀
>
> English: [README_EN.md](./README_EN.md)

## ⭐ 项目特点

| 特性 | 传统客服 | 🤖 AI 客服 |
|------|---------|-----------|
| 7×24小时服务 | ❌ 需要轮班 | ✅ 自动响应 |
| 响应速度 | 1-5分钟 | < 1秒 |
| 并发能力 | 有限 | 无限扩展 |
| 学习能力 | 需培训 | 自学习 |

## 🎯 核心功能

### 🧠 智能问答
- 基于 RAG 的向量检索，精准匹配知识库
- 支持多轮对话，上下文理解能力强
- 意图识别，自动路由到专业领域

### 📚 知识库管理
- 支持 PDF/Word/TXT/Markdown 等格式
- 自动提取文本和结构化数据
- 增量更新，实时同步

### 🔌 完整 API
- RESTful 接口，易于集成
- WebSocket 实时通信
- 管理后台 API

## 🛠 技术栈

<div align="center">

| 层级 | 技术 |
|------|------|
| **后端** | FastAPI (Python) |
| **AI 框架** | LangChain + LangGraph |
| **向量库** | Milvus / Chroma |
| **LLM** | GPT-4 / Claude / Gemini |
| **部署** | Docker / Docker Compose |

</div>

## 🚀 快速开始

### 1️⃣ 一键部署（推荐）

```bash
# 克隆项目
git clone https://github.com/ttzevol/ai-customer-service.git
cd ai-customer-service

# 启动所有服务
docker-compose up -d --build
```

### 2️⃣ 本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 .\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 编辑 .env 填入你的配置

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

## 📡 API 示例

```bash
# 发送对话
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你们有哪些功能？", "session_id": "user_123"}'

# 上传知识库
curl -X POST "http://localhost:8000/api/v1/knowledge/upload" \
  -F "file=@manual.pdf"
```

## 📈 发展路线

```
v0.1.0 (当前) → v0.2.0 → v1.0.0 → v2.0.0
  ✅ MVP        🔄 多轮对话   📦 完整产品   🌐 多语言
```

## 🤝 贡献

欢迎开发者贡献代码！

1. Fork 本仓库
2. 创建分支 `git checkout -b feature/amazing`
3. 提交改动 `git commit -m 'Add amazing feature'`
4. 推送到分支 `git push origin feature/amazing`
5. 打开 Pull Request

## 📄 许可证

MIT License - 免费商用，无需授权！

## ⭐ 如果有帮助，请 Star 支持！

```bash
# 你的支持是我最大的动力！
gh repo star ttzevol/ai-customer-service
```

---

<p align="center">
  用 ❤️ 构建 | Made with ❤️
</p>

<div align="center">

[![Star History](https://api.star-history.com/svg?repos=ttzevol/ai-customer-service&type=Date)](https://star-history.com/#ttzevol/ai-customer-service&Date)

</div>
