#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== 阿里云 IP 白名单更新工具 - 安装脚本 ===${NC}\n"

# 检查 Python 版本
echo "检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ 找到 Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ 未找到 Python 3${NC}"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

# 检查 pip
echo "检查 pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 已安装${NC}"
else
    echo -e "${RED}✗ pip3 未安装${NC}"
    exit 1
fi

# 安装依赖
echo -e "\n安装 Python 依赖..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 依赖安装成功${NC}"
else
    echo -e "${RED}✗ 依赖安装失败${NC}"
    exit 1
fi

# 创建配置文件
echo -e "\n配置文件设置..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ 创建 .env 文件${NC}"
    echo -e "${YELLOW}⚠ 请编辑 .env 文件并填入你的阿里云密钥${NC}"
else
    echo -e "${YELLOW}! .env 文件已存在，跳过${NC}"
fi

if [ ! -f config.yml ]; then
    cp config.example.yml config.yml
    echo -e "${GREEN}✓ 创建 config.yml 文件${NC}"
    echo -e "${YELLOW}⚠ 请编辑 config.yml 文件并配置你的实例${NC}"
else
    echo -e "${YELLOW}! config.yml 文件已存在，跳过${NC}"
fi

# 创建日志目录
echo -e "\n创建日志目录..."
LOG_DIR="$HOME/log/aliyun-update-security-ips"
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✓ 日志目录创建完成: $LOG_DIR${NC}"

# 安装开发工具（可选）
echo -e "\n是否安装开发工具？(y/N)"
read -r INSTALL_DEV
if [[ "$INSTALL_DEV" =~ ^[Yy]$ ]]; then
    pip3 install flake8 pylint black isort pre-commit
    pre-commit install
    echo -e "${GREEN}✓ 开发工具安装完成${NC}"
fi

# 完成
echo -e "\n${GREEN}=== 安装完成！===${NC}"
echo -e "\n下一步："
echo -e "1. 编辑 ${YELLOW}.env${NC} 文件，填入阿里云密钥"
echo -e "2. 编辑 ${YELLOW}config.yml${NC} 文件，配置实例信息"
echo -e "3. 运行 ${YELLOW}python3 update.py${NC} 进行测试"
echo -e "4. 或运行 ${YELLOW}make run-daemon${NC} 启动后台自动更新\n"

echo -e "${YELLOW}注意：请妥善保管 .env 文件，不要泄露密钥！${NC}\n"
