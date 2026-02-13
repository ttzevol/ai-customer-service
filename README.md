# AI Customer Service Bot - 智能客服机器人

基于LangGraph + RAG的企业级智能客服系统，支持知识库管理和多轮对话。

## 🛠️ 技术栈

- **后端框架**: FastAPI
- **AI框架**: LangChain, LangGraph
- **向量数据库**: Milvus / Chroma
- **LLM**: OpenAI GPT-4 / Claude / Gemini
- **部署**: Docker, Docker Compose

## 📦 安装

```bash
# 克隆项目
git clone <repo-url>
cd ai-customer-service

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动Milvus（可选）
docker-compose up -d milvus
```

## ⚙️ 配置

复制 `.env.example` 为 `.env` 并填写配置：

```bash
OPENAI_API_KEY=your_api_key_here
MILVUS_HOST=localhost
MILVUS_PORT=19530
DATABASE_URL=sqlite:///./data.db
```

## 🚀 运行

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用脚本
python scripts/run_dev.py
```

访问 http://localhost:8000/docs 查看API文档。

## 📡 API端点

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/v1/chat | 发送对话消息 |
| POST | /api/v1/knowledge/upload | 上传知识库文档 |
| GET | /api/v1/knowledge/list | 列出知识库文档 |
| GET | /api/v1/history/{session_id} | 获取对话历史 |

## 🐳 Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📁 项目结构

```
ai-customer-service/
├── app/
│   ├── api/              # FastAPI路由
│   ├── core/             # 配置和工具
│   ├── models/            # 数据模型
│   ├── services/          # 业务逻辑
│   ├── graph/             # LangGraph工作流
│   └── knowledge/         # 知识库管理
├── tests/                 # 测试用例
├── scripts/               # 部署脚本
├── docs/                  # 文档
├── docker-compose.yml     # Docker配置
├── requirements.txt       # Python依赖
└── README.md             # 项目说明
```

## 💰 定价方案

| 方案 | 价格 | 调用次数 |
|------|------|---------|
| Free | ¥0 | 100次/月 |
| Pro | ¥99/月 | 无限 |
| Enterprise | ¥299/月 | 无限+定制 |

## 📈 路线图

- [x] MVP版本发布
- [ ] LangGraph工作流集成
- [ ] 多轮对话支持
- [ ] 用户管理系统
- [ ] API文档完善
- [ ] 生产环境部署

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系

- 项目主页: https://github.com/your-repo
- 问题反馈: https://github.com/your-repo/issues
