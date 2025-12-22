# aliyun-update-security-ips

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/Kenrick-Zhou/aliyun-update-security-ips?style=social)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Kenrick-Zhou/aliyun-update-security-ips?style=social)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Kenrick-Zhou/aliyun-update-security-ips)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/issues)
[![Last Commit](https://img.shields.io/github/last-commit/Kenrick-Zhou/aliyun-update-security-ips)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/commits/main)
[![Code Size](https://img.shields.io/github/languages/code-size/Kenrick-Zhou/aliyun-update-security-ips)](https://github.com/Kenrick-Zhou/aliyun-update-security-ips)

中文 | [English](README.en.md)

</div>

自动定期（或手动）更新阿里云 RDS、Tair(Redis) 的安全IP白名单

方便DDNS环境下的服务器访问 或个人在外的访问，兼顾安全和便捷

_支持阿里云 RDS 和 Tair (Redis) 实例的安全IP白名单自动更新。
欢迎改造共建。_

## ✨ 特性

- 🔄 自动定期更新安全IP白名单
- 🎯 支持 RDS 和 Tair(Redis) 实例
- 📱 支持多种推送通知方式（Bark、PushDeer）
- ⚡ 适用于 DDNS 环境
- 🛡️ 安全便捷的访问管理
- 📝 详细的日志记录


## 用法

### 1. 配置阿里云密钥

首先需要配置阿里云的访问密钥：

1. 复制 `.env.example` 文件为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的阿里云密钥：
   ```bash
   # 阿里云 Access Key ID
   ALY_AK=your_access_key_id_here

   # 阿里云 Access Key Secret
   ALY_SK=your_access_key_secret_here

   # （可选）通知服务密钥
   # Bark 推送服务
   BARK_KEY=https://api.day.app/your_bark_key_here

   # PushDeer 推送服务
   PUSHDEER_KEY=your_pushdeer_key_here
   ```

> ⚠️ 注意：`.env` 文件包含敏感信息，请勿提交到版本控制系统中！

### 2. 配置功能参数

1. 复制 `config.example.yml` 文件为 `config.yml`：
   ```bash
   cp config.example.yml config.yml
   ```

2. 编辑 `config.yml` 文件，配置 RDS 实例、域名等信息。

### 3. 配置通知（可选）

程序支持在 IP 变更时发送通知到手机，目前支持以下通知方式：

#### 3.1 Bark 推送（推荐）

[Bark](https://bark.day.app) 是一款 iOS 推送通知应用，支持自建服务器。

1. 在 App Store 下载 Bark 应用
2. 打开应用，复制你的推送地址（直接复制完整地址即可，代码会自动处理末尾的 `/`）
3. 在 `.env` 文件中配置：
   ```bash
   BARK_KEY=https://api.day.app/your_key
   ```
4. 在 `config.yml` 中启用：
   ```yaml
   Notification:
     enabled: true
     type: bark
   ```

#### 3.2 PushDeer 推送

[PushDeer](https://www.pushdeer.com/) 是一款开源的推送服务。

1. 注册 PushDeer 账号并获取 pushkey
2. 在 `.env` 文件中配置：
   ```bash
   PUSHDEER_KEY=your_pushdeer_key
   ```
3. 在 `config.yml` 中启用：
   ```yaml
   Notification:
     enabled: true
     type: pushdeer
   ```

#### 3.3 禁用通知

默认情况下通知是关闭的，如需禁用：
```yaml
Notification:
  enabled: false
  type: none
```

### 4. 运行程序

#### 手动更新（一次性）
适用于笔记本电脑带在外面需要临时访问的场景：
```bash
python update.py
```

#### 后台自动更新（推荐）
适用于家中服务器等 DDNS 环境，自动定期检查并更新：
```bash
# 方式 1：使用 nohup 后台运行
nohup python updated.py > nohup.out 2>&1 &

# 方式 2：使用 Makefile（更方便）
make run-daemon

# 检查运行状态
make check-daemon

# 停止后台运行
make stop-daemon
```

#### 使用系统服务（推荐生产环境）

**Linux systemd 服务**
```bash
sudo nano /etc/systemd/system/aliyun-ip-updater.service
```

添加以下内容（替换路径和用户）：
```ini
[Unit]
Description=Aliyun Security IP Auto Updater
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/aliyun-update-security-ips
ExecStart=/usr/bin/python3 /path/to/aliyun-update-security-ips/updated.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable aliyun-ip-updater
sudo systemctl start aliyun-ip-updater
sudo systemctl status aliyun-ip-updater
```

**macOS launchd 服务**
```bash
nano ~/Library/LaunchAgents/com.aliyun.ipupdater.plist
```

添加以下内容（替换路径）：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aliyun.ipupdater</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/aliyun-update-security-ips/updated.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/aliyun-update-security-ips</string>
</dict>
</plist>
```

加载服务：
```bash
launchctl load ~/Library/LaunchAgents/com.aliyun.ipupdater.plist
launchctl start com.aliyun.ipupdater
```

### 配置文件说明

`config.yml` 配置示例：

```yaml
check_interval: 90  # 检查间隔（秒）

RDS:
  AutoUpdate:  # 自动定时更新配置
    ArrayName: home  # 白名单分组名称（要提前创建好）
    DBInstanceIds: &all_instance  # 要修改的RDS实例ID
      - rm-xxx
  ManualUpdate:  # 手动更新配置
    ArrayName: my
    DBInstanceIds: # 要修改的RDS实例ID
      *all_instance

Tair:  # Tair (Redis) 实例配置
  AutoUpdate:  # 自动定时更新配置
    GroupName: home  # 安全IP白名单分组名称（要提前创建好）
    InstanceIds: &all_tair_instance  # 要修改的Tair(Redis)实例ID
      - r-xxx
  ManualUpdate:  # 手动更新配置
    GroupName: my
    InstanceIds: # 要修改的Tair(Redis)实例ID
      *all_tair_instance

IPCheckList:  # 查看本机公网IP的网址
  - https://ip.clang.cn/
  - http://icanhazip.com
  - https://ipecho.net/plain
  - http://whatismyip.akamai.com/
  - https://tnx.nl/ip
  - https://www.trackip.net/ip
  - http://ip.cip.cc/

Notification:  # 通知配置（可选）
  enabled: false  # 是否启用通知，默认 false
  type: none  # 通知类型：none（不通知）、bark、pushdeer
  # type 为 bark 时，需要在 .env 中配置 BARK_KEY
  # type 为 pushdeer 时，需要在 .env 中配置 PUSHDEER_KEY

log:  # 日志存放位置（会自动创建相应目录）
  path_dir: ~/log/aliyun-update-security-ips
  path_info: ~/log/aliyun-update-security-ips/info
  path_err: ~/log/aliyun-update-security-ips/err
```

## 🚀 快速开始（使用 Makefile）

项目提供了便捷的 Makefile 命令：

```bash
# 查看所有可用命令
make help

# 初始化配置文件
make setup

# 安装依赖
make install

# 手动运行一次
make run-manual

# 后台运行
make run-daemon

# 检查后台进程
make check-daemon

# 停止后台进程
make stop-daemon
```

## 📋 常见问题

<details>
<summary><b>Q: 如何获取阿里云 Access Key？</b></summary>

1. 登录阿里云控制台
2. 点击右上角头像，选择 "AccessKey 管理"
3. 创建 AccessKey，记录 Access Key ID 和 Access Key Secret
4. ⚠️ 注意保管好密钥，不要泄露

</details>

<details>
<summary><b>Q: 如何查看 RDS/Tair 实例 ID？</b></summary>

- **RDS**: 控制台 → 云数据库 RDS → 实例列表 → 实例 ID（格式：rm-xxx）
- **Tair**: 控制台 → 云数据库 Redis → 实例列表 → 实例 ID（格式：r-xxx）

</details>

<details>
<summary><b>Q: 白名单分组需要提前创建吗？</b></summary>

是的，需要在阿里云控制台中提前创建好白名单分组：
- 进入 RDS/Tair 实例详情
- 数据安全性 → 白名单设置
- 创建白名单分组（如 `home`、`my`）

</details>

<details>
<summary><b>Q: 支持多个实例吗？</b></summary>

完全支持！在配置文件中可以添加多个实例 ID：
```yaml
DBInstanceIds:
  - rm-instance1
  - rm-instance2
  - rm-instance3
```

</details>

<details>
<summary><b>Q: 如何查看运行日志？</b></summary>

日志文件位于配置文件中指定的路径：
```bash
# 查看信息日志
tail -f ~/log/aliyun-update-security-ips/info

# 查看错误日志
tail -f ~/log/aliyun-update-security-ips/err

# 如果使用 nohup
tail -f nohup.out
```

</details>

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解如何开始。

无论是报告 bug、提出新功能建议，还是提交代码，我们都非常欢迎。

查看 [行为准则](CODE_OF_CONDUCT.md) 了解社区规范。

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史和更新内容。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐！

[![Star History Chart](https://api.star-history.com/svg?repos=Kenrick-Zhou/aliyun-update-security-ips&type=Date)](https://star-history.com/#Kenrick-Zhou/aliyun-update-security-ips&Date)

## 🙏 致谢

- 感谢阿里云提供的 SDK
- 感谢所有贡献者的努力
- 感谢使用和支持本项目的每一位用户

## 📧 联系方式

- 提交 Issue: [GitHub Issues](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/issues)
- Pull Request: [GitHub PRs](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/pulls)

---

<div align="center">

**如果觉得这个项目不错，别忘了给个 ⭐ Star 支持一下！**

Made with ❤️ by [Kenrick-Zhou](https://github.com/Kenrick-Zhou)

</div>
