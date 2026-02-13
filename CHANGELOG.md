# 📋 Changelog

所有值得注意的变更都会记录在这个文件中。

格式遵循 [Keep a Changelog](https://keepachangelog.com/)。

## [0.1.0] - 2026-02-12

### 🎉 首次发布

#### ✨ 新功能
- 基础 RAG 问答系统
- 知识库上传功能（支持 PDF/Word/TXT）
- FastAPI RESTful 接口
- Docker 容器化部署
- LangGraph 工作流准备

#### 🛠 技术栈
- FastAPI - 高性能 Web 框架
- LangChain + LangGraph - AI 工作流
- Milvus / Chroma - 向量数据库
- OpenAI GPT-4 - 大语言模型
- Docker - 容器化部署

#### 📦 包含组件
- 对话接口 (`/api/v1/chat`)
- 知识库接口 (`/api/v1/knowledge/*`)
- 健康检查接口 (`/api/v1/health`)
- Docker Compose 配置
- 完整的测试用例

#### 📝 文档
- README.md - 项目说明
- PROJECT.md - 开发计划
- MARKETING.md - 营销方案
- USER_GUIDE.md - 使用指南
- CONTRIBUTING.md - 贡献指南

---

## 如何贡献

如果你修复了 Bug 或添加了新功能，请按照以下格式添加条目：

```markdown
## [版本号] - 日期

### 🚀 新功能
- 功能描述

### 🐛 Bug 修复
- 修复描述

### 📚 文档
- 文档更新

### ⚡ 性能优化
- 优化描述
```

---

**感谢每一位贡献者！** 🎉
