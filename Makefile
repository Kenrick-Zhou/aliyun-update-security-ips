.PHONY: help install test lint format clean

help:  ## 显示帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安装依赖
	pip install -r requirements.txt

install-dev:  ## 安装开发依赖
	pip install -r requirements.txt
	pip install flake8 pylint black isort pre-commit
	pre-commit install

test:  ## 运行测试
	python test_notifications.py

lint:  ## 代码检查
	flake8 *.py
	pylint *.py

format:  ## 格式化代码
	black --line-length 120 *.py
	isort --profile black *.py

clean:  ## 清理临时文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/

setup:  ## 初始化配置文件
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ 已创建 .env 文件，请编辑并填入你的密钥"; \
	fi
	@if [ ! -f config.yml ]; then \
		cp config.example.yml config.yml; \
		echo "✓ 已创建 config.yml 文件，请编辑并配置你的实例"; \
	fi

run-manual:  ## 手动运行一次更新
	python update.py

run-daemon:  ## 后台运行定期更新
	nohup python updated.py > nohup.out 2>&1 &
	@echo "已在后台启动，日志文件: nohup.out"

stop-daemon:  ## 停止后台运行
	pkill -f updated.py
	@echo "已停止后台进程"

check-daemon:  ## 检查后台进程状态
	@ps aux | grep updated.py | grep -v grep || echo "未找到运行中的进程"
