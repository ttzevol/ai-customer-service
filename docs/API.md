# 📡 API 文档

> 本文档描述 AI Customer Service Bot 的 RESTful API 接口。

## 📋 基础信息

- **Base URL**: `http://localhost:8000`
- **文档地址**: `http://localhost:8000/docs` (Swagger UI)
- **认证**: Bearer Token（可选，当前版本未启用）

---

## 💬 对话接口

### 发送对话消息

**POST** `/api/v1/chat`

#### 请求参数

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `message` | string | ✅ | 用户输入的消息 |
| `session_id` | string | ✅ | 会话 ID，用于追踪对话 |
| `metadata` | object | ❌ | 附加元数据 |

#### 请求示例

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你们的定价是怎样的？",
    "session_id": "user_123",
    "metadata": {"source": "website"}
  }'
```

#### 响应示例

```json
{
  "success": true,
  "data": {
    "response": "我们有三个定价方案：\n\n1. Free - ¥0/月，100次调用\n2. Pro - ¥99/月，无限调用\n3. Enterprise - ¥299/月，无限+定制",
    "session_id": "user_123",
    "timestamp": "2025-02-12T10:30:00Z"
  }
}
```

---

## 📚 知识库接口

### 上传文档

**POST** `/api/v1/knowledge/upload`

#### 请求参数 (multipart/form-data)

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `file` | File | ✅ | 要上传的文档 |
| `category` | string | ❌ | 分类标签 |

#### 请求示例

```bash
curl -X POST "http://localhost:8000/api/v1/knowledge/upload" \
  -F "file=@manual.pdf" \
  -F "category=product"
```

#### 响应示例

```json
{
  "success": true,
  "data": {
    "id": "doc_abc123",
    "filename": "manual.pdf",
    "status": "processing",
    "message": "文档已上传，正在处理..."
  }
}
```

### 列出文档

**GET** `/api/v1/knowledge/list`

#### 请求参数 (Query)

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `category` | string | ❌ | 按分类筛选 |
| `page` | int | ❌ | 页码，默认 1 |
| `page_size` | int | ❌ | 每页数量，默认 10 |

#### 请求示例

```bash
curl "http://localhost:8000/api/v1/knowledge/list?page=1&page_size=10"
```

#### 响应示例

```json
{
  "success": true,
  "data": {
    "documents": [
      {
        "id": "doc_abc123",
        "filename": "manual.pdf",
        "category": "product",
        "status": "ready",
        "created_at": "2025-02-12T10:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10
  }
}
```

### 删除文档

**DELETE** `/api/v1/knowledge/{doc_id}`

#### 请求示例

```bash
curl -X DELETE "http://localhost:8000/api/v1/knowledge/doc_abc123"
```

---

## 🔍 对话历史接口

### 获取历史

**GET** `/api/v1/history/{session_id}`

#### 请求示例

```bash
curl "http://localhost:8000/api/v1/history/user_123"
```

#### 响应示例

```json
{
  "success": true,
  "data": {
    "session_id": "user_123",
    "messages": [
      {
        "role": "user",
        "content": "你们有哪些功能？",
        "timestamp": "2025-02-12T10:29:00Z"
      },
      {
        "role": "assistant",
        "content": "我们提供智能问答、多轮对话、知识库管理等功能。",
        "timestamp": "2025-02-12T10:29:01Z"
      }
    ]
  }
}
```

---

## 💚 健康检查接口

### 检查状态

**GET** `/api/v1/health`

#### 响应示例

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "0.1.0",
    "timestamp": "2025-02-12T10:30:00Z"
  }
}
```

---

## ⚠️ 错误响应

所有接口的错误响应格式：

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

### 常见错误码

| 错误码 | 描述 |
|--------|------|
| `VALIDATION_ERROR` | 参数验证失败 |
| `NOT_FOUND` | 资源不存在 |
| `INTERNAL_ERROR` | 服务器内部错误 |
| `RATE_LIMITED` | 请求过于频繁 |

---

## 📝 备注

1. 所有时间戳使用 **UTC** 时区
2. 响应中的 `success` 字段表示请求是否成功
3. 建议在请求头中添加 `Content-Type: application/json`

---

## 🔗 相关链接

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)
- [项目 GitHub](https://github.com/ttzevol/ai-customer-service)
