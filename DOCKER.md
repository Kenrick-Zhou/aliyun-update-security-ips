# Docker 支持（计划中）

> 注意：Docker 支持目前还在计划中，预计在 v2.1 版本提供。

## 计划的 Docker 功能

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "updated.py"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  aliyun-ip-updater:
    build: .
    container_name: aliyun-ip-updater
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./config.yml:/app/config.yml
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
```

### 使用方式
```bash
# 构建镜像
docker build -t aliyun-ip-updater .

# 运行容器
docker run -d \
  --name aliyun-ip-updater \
  --restart unless-stopped \
  -v $(pwd)/config.yml:/app/config.yml \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  aliyun-ip-updater

# 查看日志
docker logs -f aliyun-ip-updater
```

### Docker Hub
计划发布到 Docker Hub:
```bash
docker pull kenrick/aliyun-ip-updater:latest
```

## 时间线

- v2.0: 基础 Docker 支持
- v2.1: Docker Compose 配置
- v2.2: Kubernetes 部署示例

## 贡献

如果你对 Docker 支持感兴趣，欢迎：
- 提交 Issue 讨论需求
- 贡献 Dockerfile
- 测试和反馈

---

> 关注 [ROADMAP.md](ROADMAP.md) 了解最新进展。
