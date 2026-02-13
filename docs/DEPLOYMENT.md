# 🚀 生产环境部署指南

本指南介绍如何在生产环境部署 AI Customer Service Bot。

## 📋 目录

- [环境要求](#环境要求)
- [服务器配置](#服务器配置)
- [Docker 部署](#docker-部署)
- [Nginx 配置](#nginx-配置)
- [HTTPS 证书](#https-证书)
- [监控和日志](#监控和日志)
- [备份和恢复](#备份和恢复)

---

## 🖥️ 环境要求

### 最低配置

| 资源 | 最低 | 推荐 |
|------|------|------|
| CPU | 2 核 | 4 核 |
| 内存 | 4 GB | 8 GB |
| 磁盘 | 20 GB | 50 GB SSD |
| 带宽 | 1 Mbps | 5 Mbps |

### 推荐配置（支持 100 并发）

| 资源 | 配置 |
|------|------|
| CPU | 4 核 |
| 内存 | 16 GB |
| 磁盘 | 100 GB SSD |
| 带宽 | 10 Mbps |

---

## 🔧 服务器配置

### 1. 系统更新

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. 安装 Docker

```bash
# Ubuntu
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 验证安装
docker --version
docker-compose --version
```

### 3. 配置防火墙

```bash
# Ubuntu (ufw)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

---

## 🐳 Docker 部署

### 1. 克隆项目

```bash
git clone https://github.com/ttzevol/ai-customer-service.git
cd ai-customer-service
```

### 2. 配置环境变量

```bash
# 创建生产环境配置
cp .env.example .env.production

# 编辑配置
nano .env.production
```

**生产环境配置示例：**

```bash
# 必须修改的配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
MILVUS_HOST=milvus-standalone
MILVUS_PORT=19530

# 数据库配置
DATABASE_URL=postgresql://user:password@db:5432/ai_customer_service

# Redis 配置（可选，用于缓存）
REDIS_HOST=redis
REDIS_PORT=6379

# 应用配置
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
WORKERS=4
PORT=8000
```

### 3. 配置 Docker Compose

```bash
# 编辑生产环境配置
nano docker-compose.prod.yml
```

**生产环境配置：**

```yaml
version: '3.8'

services:
  app:
    build: .
    restart: always
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MILVUS_HOST=milvus-standalone
      - MILVUS_PORT=19530
    depends_on:
      - milvus-standalone
      - redis
      - db
    volumes:
      - app_data:/app/data
      - uploads:/app/uploads
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  milvus-standalone:
    image: milvusdb/milvus:latest
    restart: always
    ports:
      - "19530:19530"
    volumes:
      - milvus_data:/var/lib/milvus

  redis:
    image: redis:7-alpine
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: ai_customer_service
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app

volumes:
  app_data:
  milvus_data:
  redis_data:
  postgres_data:
```

### 4. 启动服务

```bash
# 构建并启动
docker-compose -f docker-compose.prod.yml up -d --build

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 检查状态
docker-compose -f docker-compose.prod.yml ps
```

---

## 🌐 Nginx 配置

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    server {
        listen 80;
        server_name your-domain.com;

        # 重定向到 HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL 证书
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/private.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;

        # 安全头
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # API 代理
        location /api {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 300s;
            proxy_connect_timeout 75s;
        }

        # 健康检查
        location /health {
            proxy_pass http://app;
            proxy_set_header Host $host;
        }

        # 静态文件（如果有）
        location /static {
            alias /app/static;
        }
    }
}
```

---

## 🔒 HTTPS 证书

### 使用 Let's Encrypt（免费）

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

### 自动续期

```bash
# 添加 cron 任务
sudo crontab -e

# 添加以下行（每天凌晨2点检查续期）
0 2 * * * certbot renew --quiet
```

---

## 📊 监控和日志

### 1. Docker 日志

```bash
# 查看应用日志
docker-compose -f docker-compose.prod.yml logs -f app

# 查看最近 100 行
docker-compose -f docker-compose.prod.yml logs --tail 100 app
```

### 2. 健康检查

```bash
# API 健康检查
curl https://your-domain.com/api/v1/health

# 预期响应
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "0.1.0"
  }
}
```

### 3. 资源监控

```bash
# Docker 资源使用
docker stats

# 磁盘使用
df -h

# 内存使用
free -m
```

### 4. 日志管理

```bash
# 日志轮转配置 /etc/logrotate.d/docker
/var/lib/docker/containers/**/*.log {
    daily
    rotate 7
    copytruncate
    compress
    delaycompress
    missingok
}
```

---

## 💾 备份和恢复

### 1. 数据库备份

```bash
# PostgreSQL 备份
docker exec -it ai-customer-service-db pg_dump -U user ai_customer_service > backup_$(date +%Y%m%d).sql

# 定时备份（每天凌晨3点）
0 3 * * * docker exec ai-customer-service-db pg_dump -U user ai_customer_service | gzip > /backup/db_$(date +\%Y\%m\%d).sql.gz
```

### 2. Milvus 数据备份

```bash
# 备份向量数据
docker cp ai-customer-service-milvus-standalone:/var/lib/milvus /backup/milvus_$(date +%Y%m%d)
```

### 3. 恢复数据

```bash
# 恢复 PostgreSQL
docker exec -i ai-customer-service-db psql -U user ai_customer_service < backup_20260101.sql
```

---

## ⚡ 性能优化

### 1. 应用层

```bash
# 增加 worker 进程数
WORKERS=4

# 启用 uvicorn 异步
UVICORN_WORKERS=4
UVICORN_ASYNC=true
```

### 2. 数据库优化

```sql
-- PostgreSQL 优化配置
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';
ALTER SYSTEM SET work_mem = '256MB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
```

### 3. Redis 缓存

```python
# 缓存热点数据
CACHE_TTL = 3600  # 1小时
```

---

## 🚨 故障排查

### 问题 1：服务无法启动

```bash
# 检查错误日志
docker-compose -f docker-compose.prod.yml logs

# 常见原因：
# 1. 端口被占用 → 修改端口映射
# 2. 内存不足 → 增加服务器内存
# 3. 环境变量缺失 → 检查 .env.production
```

### 问题 2：数据库连接失败

```bash
# 检查数据库状态
docker-compose -f docker-compose.prod.yml ps db

# 检查连接
docker exec -it ai-customer-service-db psql -U user -d ai_customer_service
```

### 问题 3：Milvus 向量检索慢

```bash
# 检查 Milvus 状态
docker exec -it ai-customer-service-milvus-standalone milvusctl status

# 优化建议：
# 1. 增加 Milvus 内存
# 2. 使用 GPU 版本
# 3. 优化索引参数
```

---

## 📞 技术支持

遇到问题？

1. 查看文档：[docs/USER_GUIDE.md](./USER_GUIDE.md)
2. 查看 API 文档：http://your-domain.com/docs
3. 提交 Issue：https://github.com/ttzevol/ai-customer-service/issues

---

## ✅ 部署检查清单

- [ ] 服务器准备完成
- [ ] Docker 安装完成
- [ ] 环境变量配置完成
- [ ] SSL 证书配置完成
- [ ] 防火墙配置完成
- [ ] 监控配置完成
- [ ] 备份策略配置完成
- [ ] 健康检查通过
- [ ] 压力测试通过

---

**祝你部署顺利！** 🎉
