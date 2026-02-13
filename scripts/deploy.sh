#!/bin/bash
# Production Deployment Script - 生产环境部署脚本

set -e

echo "🚀 开始部署 AI Customer Service Bot..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker 未安装，请先安装 Docker${NC}"
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env 文件不存在，创建模板...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  请编辑 .env 文件填入 API Key！${NC}"
    exit 1
fi

# 检查 API Key
if grep -q "your_openai_api_key_here" .env; then
    echo -e "${RED}❌ 请在 .env 文件中设置 OPENAI_API_KEY${NC}"
    exit 1
fi

# 创建必要目录
echo -e "${GREEN}📁 创建数据目录...${NC}"
mkdir -p data/milvus data/chroma logs

# 停止旧容器
echo -e "${GREEN}🛑 停止旧容器...${NC}"
docker-compose down --remove-orphans 2>/dev/null || true

# 构建并启动
echo -e "${GREEN">#️⃣ 构建并启动服务...
docker-compose up -d --build

# 等待服务启动
echo -e "${GREEN}⏳ 等待服务启动...${NC}"
sleep 10

# 检查健康状态
echo -e "${GREEN}🔍 检查服务状态...${NC}"
curl -s http://localhost:8000/health || {
    echo -e "${RED}❌ 服务启动失败，查看日志：docker-compose logs${NC}"
    exit 1
}

echo -e "${GREEN}✅ 部署完成！${NC}"
echo ""
echo "📚 API文档: http://localhost:8000/docs"
echo "🏥 健康检查: http://localhost:8000/health"
echo "📝 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"
