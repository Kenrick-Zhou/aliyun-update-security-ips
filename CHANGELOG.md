# 更新日志

所有值得注意的项目变更都将记录在此文件中。

本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)规范。

## [Unreleased]

### 新增
- 添加完整的项目文档和开源社区文件
  - README badges 展示项目状态
  - 贡献指南 (CONTRIBUTING.md)
  - 行为准则 (CODE_OF_CONDUCT.md)
  - Issue 和 PR 模板
  - GitHub Actions 工作流
  - 代码质量配置文件

## [1.0.0] - 2022-XX-XX

### 新增
- 支持自动更新阿里云 RDS 安全IP白名单
- 支持自动更新阿里云 Tair(Redis) 安全IP白名单
- 支持 Bark 推送通知
- 支持 PushDeer 推送通知
- 定时自动检查和更新功能
- 手动更新功能
- 详细的日志记录

### 特性
- 适用于 DDNS 环境
- 支持多个 RDS 实例
- 支持多个 Tair 实例
- 灵活的配置文件

---

## 更新日志格式说明

- `新增` - 新功能
- `变更` - 现有功能的变更
- `弃用` - 即将移除的功能
- `移除` - 已移除的功能
- `修复` - Bug 修复
- `安全` - 安全相关的修复

[Unreleased]: https://github.com/Kenrick-Zhou/aliyun-update-security-ips/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Kenrick-Zhou/aliyun-update-security-ips/releases/tag/v1.0.0
