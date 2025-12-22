# 依赖项说明

本项目使用以下主要依赖：

## 核心依赖

### 阿里云 SDK
- **alibabacloud_rds20140815**: RDS 数据库实例管理
- **alibabacloud-alidns20150109**: 阿里云 DNS 管理
- **alibabacloud-r-kvstore20150101**: Redis/Tair 实例管理
- **alibabacloud_tea_openapi**: 阿里云 OpenAPI 基础库
- **alibabacloud_tea_util**: 阿里云工具库
- **alibabacloud_tea**: Tea 语言运行时

### 其他依赖
- **PyYAML**: YAML 配置文件解析
- **python-dotenv**: 环境变量管理
- **requests**: HTTP 请求库，用于获取公网 IP

## 开发依赖（可选）

```bash
pip install flake8 pylint black isort pre-commit
```

- **flake8**: Python 代码风格检查
- **pylint**: Python 代码静态分析
- **black**: Python 代码格式化工具
- **isort**: Python import 语句排序
- **pre-commit**: Git pre-commit hooks

## 安全性

所有依赖都应该定期更新以获取安全补丁：

```bash
pip install --upgrade -r requirements.txt
```

可以使用以下工具检查依赖的安全漏洞：

```bash
pip install safety
safety check -r requirements.txt
```

## 版本兼容性

- Python: 3.7+
- 建议使用虚拟环境隔离依赖

## 更新日志

依赖更新应记录在 [CHANGELOG.md](CHANGELOG.md) 中。
