# 项目结构

```
aliyun-update-security-ips/
├── .github/                      # GitHub 配置文件
│   ├── workflows/                # GitHub Actions 工作流
│   │   ├── python-lint.yml       # Python 代码检查
│   │   └── dependency-review.yml # 依赖审查
│   ├── ISSUE_TEMPLATE/           # Issue 模板
│   │   ├── bug_report.md         # Bug 报告模板
│   │   ├── feature_request.md    # 功能请求模板
│   │   └── question.md           # 问题咨询模板
│   ├── PULL_REQUEST_TEMPLATE.md  # PR 模板
│   ├── FUNDING.yml               # 赞助配置
│   └── TOPICS.md                 # GitHub Topics 建议
│
├── __pycache__/                  # Python 缓存（已忽略）
│
├── .editorconfig                 # 编辑器配置
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git 忽略规则
├── .pre-commit-config.yaml       # Pre-commit hooks 配置
│
├── CHANGELOG.md                  # 更新日志
├── CODE_OF_CONDUCT.md            # 行为准则
├── CONTRIBUTING.md               # 贡献指南
├── DEPENDENCIES.md               # 依赖说明
├── LICENSE                       # MIT 许可证
├── Makefile                      # Make 命令
├── PROJECT_STRUCTURE.md          # 本文件
├── README.md                     # 项目说明
├── ROADMAP.md                    # 项目路线图
├── SECURITY.md                   # 安全策略
│
├── config.example.yml            # 配置文件示例
├── config.yml                    # 配置文件（需自行创建）
├── requirements.txt              # Python 依赖
├── setup.cfg                     # 工具配置
│
├── init.py                       # 初始化模块
├── update.py                     # 手动更新脚本
├── updated.py                    # 自动更新脚本
└── test_notifications.py         # 通知测试脚本
```

## 文件说明

### 核心文件

#### `update.py`
手动更新脚本，运行一次后退出。适用场景：
- 临时需要访问数据库
- 笔记本电脑外出时
- 测试配置是否正确

#### `updated.py`
自动更新脚本，后台持续运行。适用场景：
- 家庭服务器（DDNS 环境）
- 需要持续保持白名单更新
- 生产环境部署

#### `init.py`
初始化模块，包含：
- 配置文件加载
- 环境变量读取
- 日志系统初始化
- 阿里云客户端配置

#### `test_notifications.py`
通知功能测试脚本，用于测试 Bark 或 PushDeer 推送是否正常工作。

### 配置文件

#### `.env`（需自行创建）
存储敏感信息：
- 阿里云 AccessKey
- 通知服务密钥
- **⚠️ 不要提交到 Git！**

#### `config.yml`（需自行创建）
功能配置：
- RDS/Tair 实例列表
- 白名单分组名称
- 检查间隔
- IP 查询服务列表
- 通知设置
- 日志路径

### 文档文件

#### `README.md`
项目主文档，包含：
- 项目简介和功能
- 安装和配置指南
- 使用方法
- 常见问题
- 贡献指南链接

#### `CONTRIBUTING.md`
贡献指南，说明如何参与项目开发。

#### `CODE_OF_CONDUCT.md`
社区行为准则，营造友好的开发环境。

#### `CHANGELOG.md`
版本更新历史记录。

#### `SECURITY.md`
安全策略和漏洞报告指南。

#### `ROADMAP.md`
项目发展路线图和计划功能。

#### `DEPENDENCIES.md`
依赖项说明和安全建议。

### GitHub 相关

#### `.github/workflows/`
GitHub Actions 自动化工作流：
- 代码质量检查
- 依赖安全审查
- 自动化测试（待实现）

#### `.github/ISSUE_TEMPLATE/`
Issue 模板，引导用户提供完整信息：
- Bug 报告
- 功能请求
- 问题咨询

#### `.github/PULL_REQUEST_TEMPLATE.md`
PR 模板，确保 PR 包含必要信息。

### 开发工具配置

#### `.editorconfig`
统一不同编辑器的代码风格：
- 缩进方式
- 字符编码
- 行尾符号

#### `.pre-commit-config.yaml`
Git pre-commit hooks，提交前自动执行：
- 代码格式化（black）
- Import 排序（isort）
- 代码检查（flake8）

#### `setup.cfg`
工具配置文件：
- flake8 规则
- pylint 配置
- mypy 类型检查

#### `Makefile`
便捷命令集合：
- 安装依赖
- 运行脚本
- 代码检查
- 格式化代码

## 使用流程

### 首次使用
1. 克隆仓库
2. 运行 `make setup` 创建配置文件
3. 编辑 `.env` 和 `config.yml`
4. 运行 `make install` 安装依赖
5. 运行 `make run-manual` 测试

### 开发流程
1. Fork 仓库
2. 创建功能分支
3. 进行开发
4. 运行 `make lint` 检查代码
5. 提交 PR

### 生产部署
1. 配置系统服务（systemd/launchd）
2. 启动服务
3. 监控日志
4. 定期更新依赖

## 日志文件

运行时会在 `config.yml` 指定的路径生成日志文件：
```
~/log/aliyun-update-security-ips/
├── info                         # 信息日志
└── err                          # 错误日志
```

## 维护建议

- 定期备份配置文件
- 关注依赖安全更新
- 监控日志中的错误
- 定期轮换 AccessKey
- 保持文档与代码同步
