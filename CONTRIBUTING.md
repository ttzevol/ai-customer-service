# 🤝 贡献指南

感谢您对 AI Customer Service Bot 项目的兴趣！我们欢迎任何形式的贡献，无论是报告问题、提出建议还是提交代码。

## 📋 目录

- [如何贡献](#-如何贡献)
- [报告问题](#报告问题)
- [提出建议](#提出建议)
- [提交代码](#提交代码)
- [代码规范](#代码规范)
- [测试](#测试)

## 📋 如何贡献

1. **Fork** 本仓库
2. **克隆** 你的 Fork 到本地：
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-customer-service.git
   ```
3. **创建分支** 进行开发：
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **提交改动**：
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **推送到你的 Fork**：
   ```bash
   git push origin feature/amazing-feature
  6. **打开 Pull Request**

## 📝 报告问题

如果发现 Bug 或问题，请：

1. 搜索是否已有相同的问题
2. 如果没有，创建新的 Issue
3. 使用问题模板，提供：
   - 清晰的标题
   - 详细的问题描述
   - 重现步骤
   - 预期行为 vs 实际行为
   - 日志/截图（如有）
   - 环境信息（Python 版本、操作系统等）

## 💡 提出建议

欢迎提出新功能建议！请：

1. 搜索是否已有相同的建议
2. 如果没有，创建新的 Issue，选择 "Feature Request" 模板
3. 详细描述：
   - 你的使用场景
   - 期望的功能
   - 可能的实现方案

## 🔧 提交代码

### 代码风格

- 遵循 **PEP 8** Python 代码规范
- 使用 **Black** 格式化代码：
  ```bash
  black .
  ```
- 使用 **isort** 排序导入：
  ```bash
  isort .
  ```
- 使用 **flake8** 检查：
  ```bash
  flake8 .
  ```

### 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**类型 (Type)：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例：**
```
feat(chat): 添加多轮对话支持

- 实现上下文记忆
- 添加对话历史管理
- 支持长文本分割

Closes #123
```

## 🧪 测试

提交代码前，请确保：

1. **编写测试**：
   ```bash
   # 添加测试到 tests/ 目录
   ```

2. **运行测试**：
   ```bash
   pytest tests/
   ```

3. **检查覆盖率**：
   ```bash
   pytest --cov=app tests/
   ```

## 📖 文档

- 更新 API 文档（如有改动）
- 添加新功能的说明
- 更新 README.md（如有必要）

## 🎯 优先级

我们优先考虑以下贡献：

- 🔥 严重 Bug 修复
- ⭐ 核心功能增强
- 📚 文档改进
- 🌍 多语言支持
- ⚡ 性能优化

## 📞 联系我们

- GitHub Issues: [https://github.com/ttzevol/ai-customer-service/issues](https://github.com/ttzevol/ai-customer-service/issues)
- 作者邮箱: [your-email@example.com](mailto:your-email@example.com)

---

再次感谢您的贡献！ 🎉
