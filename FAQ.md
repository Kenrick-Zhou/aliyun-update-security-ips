# 常见问题 (FAQ)

## 目录
- [安装和配置](#安装和配置)
- [使用问题](#使用问题)
- [错误排查](#错误排查)
- [安全相关](#安全相关)
- [功能相关](#功能相关)

---

## 安装和配置

### Q: 支持哪些 Python 版本？
**A:** Python 3.7 及以上版本。推荐使用 Python 3.9 或更高版本。

### Q: 如何获取阿里云 AccessKey？
**A:** 
1. 登录阿里云控制台
2. 鼠标悬停在右上角头像，点击 "AccessKey 管理"
3. 点击 "创建 AccessKey"
4. 保存 Access Key ID 和 Access Key Secret
5. ⚠️ 务必妥善保管，不要泄露

### Q: AccessKey 需要什么权限？
**A:** 需要以下权限：
- `AliyunRDSFullAccess` - RDS 完全访问权限
- `AliyunKvstoreFullAccess` - Redis/Tair 完全访问权限
- 或者创建自定义权限策略，只授予修改白名单的权限

### Q: 配置文件放在哪里？
**A:** 
- `.env` - 项目根目录
- `config.yml` - 项目根目录
- 日志文件 - 在 `config.yml` 中配置，默认 `~/log/aliyun-update-security-ips/`

### Q: 如何验证配置是否正确？
**A:** 运行手动更新脚本测试：
```bash
python update.py
```
查看输出信息和日志文件确认是否成功。

---

## 使用问题

### Q: `update.py` 和 `updated.py` 有什么区别？
**A:** 
- `update.py` - 运行一次后退出，适合临时需要访问时使用
- `updated.py` - 持续后台运行，定期检查和更新，适合 DDNS 环境

### Q: 如何让程序开机自启动？
**A:** 
- **Linux**: 使用 systemd 服务（参考 README）
- **macOS**: 使用 launchd（参考 README）
- **Windows**: 使用任务计划程序

### Q: 检查间隔多久合适？
**A:** 
- DDNS 环境：建议 60-300 秒
- 稳定网络：建议 300-600 秒
- 注意：间隔太短可能触发 API 限流

### Q: 支持多个实例吗？
**A:** 完全支持。在 `config.yml` 中可以配置多个 RDS 和 Tair 实例。

### Q: 白名单分组需要提前创建吗？
**A:** 是的，需要在阿里云控制台中提前创建白名单分组。

### Q: 可以同时使用 RDS 和 Tair 吗？
**A:** 可以。配置文件中同时配置即可。

---

## 错误排查

### Q: 提示 "Cannot get IP"
**A:** 可能的原因：
1. 网络连接问题
2. IP 查询服务不可用
3. 防火墙阻止了外网访问

解决方法：
- 检查网络连接
- 在 `config.yml` 中添加更多 IP 查询服务
- 检查防火墙设置

### Q: 提示 AccessKey 错误
**A:** 
- 确认 `.env` 文件中的密钥是否正确
- 确认密钥是否过期
- 确认密钥是否有足够权限
- 检查是否有多余的空格或换行

### Q: 提示实例 ID 不存在
**A:** 
- 确认实例 ID 格式正确（RDS: rm-xxx, Tair: r-xxx）
- 确认实例在正确的地域
- 确认 AccessKey 有访问该实例的权限

### Q: 提示白名单分组不存在
**A:** 
- 在阿里云控制台提前创建该分组
- 确认分组名称拼写正确
- 注意分组名称区分大小写

### Q: 日志文件没有生成
**A:** 
- 确认日志路径有写入权限
- 确认路径中的目录存在或程序有创建目录的权限
- 检查 `config.yml` 中的日志路径配置

### Q: 后台进程无法启动
**A:** 
- 检查是否已有进程在运行
- 查看 `nohup.out` 或日志文件中的错误信息
- 确认 Python 路径正确
- 使用 `make check-daemon` 检查进程状态

---

## 安全相关

### Q: `.env` 文件安全吗？
**A:** 
- `.env` 包含敏感信息，已在 `.gitignore` 中排除
- 不要提交到版本控制系统
- 设置适当的文件权限（Linux/macOS: `chmod 600 .env`）
- 考虑使用环境变量或密钥管理服务

### Q: 如何保护 AccessKey？
**A:** 
1. 定期轮换密钥
2. 使用最小权限原则
3. 不要在日志中记录密钥
4. 不要提交到 Git
5. 考虑使用 RAM 角色（如果在 ECS 上运行）

### Q: 程序会保存 IP 历史吗？
**A:** 目前不会。程序只在内存中比较 IP 变化，不保存历史记录。

### Q: 通知消息会包含敏感信息吗？
**A:** 通知消息只包含 IP 地址和实例 ID，不包含 AccessKey 等敏感信息。

---

## 功能相关

### Q: 支持哪些通知方式？
**A:** 目前支持：
- Bark（iOS）
- PushDeer（跨平台）
- 计划支持：微信、钉钉、Telegram、Email

### Q: 如何测试通知功能？
**A:** 运行测试脚本：
```bash
python test_notifications.py
```

### Q: IP 变化时一定会发通知吗？
**A:** 只有在配置文件中启用通知（`Notification.enabled: true`）且配置正确时才会发送。

### Q: 支持 IPv6 吗？
**A:** 目前仅支持 IPv4。IPv6 支持在计划中。

### Q: 支持多地域实例吗？
**A:** 支持。阿里云 SDK 会自动处理不同地域的实例。

### Q: 可以自定义 IP 获取源吗？
**A:** 可以。在 `config.yml` 的 `IPCheckList` 中添加你信任的 IP 查询服务。

### Q: 支持 DNS 解析吗？
**A:** 配置文件中有 DNS 相关配置，但可能需要额外设置。详见配置文件注释。

### Q: 会自动创建白名单分组吗？
**A:** 不会。需要手动在阿里云控制台创建。

### Q: 支持删除旧 IP 吗？
**A:** 程序会更新白名单分组的 IP，新 IP 会替换旧 IP。

---

## 性能相关

### Q: 对网络性能有影响吗？
**A:** 
- 影响极小
- 只在检查间隔时发起少量 HTTP/HTTPS 请求
- 建议合理设置检查间隔

### Q: 会被阿里云 API 限流吗？
**A:** 
- 如果检查间隔设置合理，一般不会
- 建议间隔不小于 60 秒
- 实例很多时适当增加间隔

### Q: 占用多少资源？
**A:** 
- CPU: 几乎可忽略（仅在检查时短暂占用）
- 内存: < 50MB
- 网络: < 1KB/次检查

---

## 其他问题

### Q: 支持 Windows 吗？
**A:** 支持，但某些功能（如 Makefile）在 Windows 上可能需要额外工具。建议使用 WSL。

### Q: 如何贡献代码？
**A:** 请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### Q: 发现 Bug 怎么办？
**A:** 请在 [GitHub Issues](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/issues) 创建 Bug 报告。

### Q: 有功能建议怎么办？
**A:** 欢迎创建 Feature Request Issue 或在 Discussions 中讨论。

### Q: 可以用于商业项目吗？
**A:** 可以。本项目采用 MIT 许可证，可自由使用。

### Q: 项目会持续维护吗？
**A:** 是的。我们会持续维护和改进项目。查看 [ROADMAP.md](ROADMAP.md) 了解未来计划。

---

## 找不到答案？

如果你的问题没有在这里找到答案：

1. 查看 [README.md](README.md) 完整文档
2. 搜索 [已有 Issues](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/issues)
3. 创建新的 [Issue](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/issues/new/choose)
4. 在 [Discussions](https://github.com/Kenrick-Zhou/aliyun-update-security-ips/discussions) 中提问

我们会尽快回复！ 😊
