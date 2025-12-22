# 维护者指南

本文档面向项目维护者，提供日常维护和发布的指导。

## 日常维护

### 代码审查

审查 PR 时检查：
- [ ] 代码符合项目风格
- [ ] 包含必要的注释
- [ ] 没有安全风险
- [ ] 更新了相关文档
- [ ] 通过所有 CI 检查
- [ ] 功能测试通过

### Issue 管理

1. **标签分类**
   - `bug`: 错误报告
   - `enhancement`: 新功能
   - `documentation`: 文档相关
   - `question`: 使用问题
   - `good first issue`: 适合新手
   - `help wanted`: 需要帮助

2. **响应时间**
   - 新 Issue: 48 小时内响应
   - Bug 报告: 优先处理
   - 功能请求: 评估可行性后回复

### 依赖更新

定期（每月）检查并更新依赖：

```bash
# 检查过时的依赖
pip list --outdated

# 检查安全漏洞
pip install safety
safety check -r requirements.txt

# 更新依赖
pip install --upgrade <package-name>

# 更新 requirements.txt
pip freeze > requirements.txt
```

## 发布流程

### 版本号规则

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：
- **主版本号**：不兼容的 API 变更
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

示例：`v1.2.3`

### 发布前检查清单

#### 1. 代码准备
- [ ] 所有 CI 测试通过
- [ ] 代码审查完成
- [ ] 没有已知的严重 bug
- [ ] 更新了版本号（如果需要）

#### 2. 文档更新
- [ ] 更新 `CHANGELOG.md`
- [ ] 更新 `README.md`（如果有功能变更）
- [ ] 更新 `requirements.txt`
- [ ] 检查示例配置文件

#### 3. 测试验证
- [ ] 本地测试通过
- [ ] 在测试环境验证
- [ ] 通知功能测试
- [ ] 多实例测试

#### 4. 安全检查
- [ ] 依赖安全扫描
- [ ] 代码安全审查
- [ ] 密钥管理检查

### 发布步骤

#### 1. 更新 CHANGELOG

```bash
# 编辑 CHANGELOG.md
vim CHANGELOG.md
```

添加新版本信息：
```markdown
## [1.2.0] - 2024-01-15

### 新增
- 功能描述

### 修复
- Bug 描述

### 变更
- 变更描述
```

#### 2. 创建发布分支（可选）

```bash
git checkout -b release/v1.2.0
```

#### 3. 提交变更

```bash
git add .
git commit -m "chore: prepare release v1.2.0"
git push origin main
```

#### 4. 创建 Git Tag

```bash
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
```

#### 5. 创建 GitHub Release

1. 访问 `https://github.com/Kenrick-Zhou/aliyun-update-security-ips/releases`
2. 点击 "Draft a new release"
3. 选择刚创建的 tag
4. 填写发布标题：`v1.2.0 - 简短描述`
5. 复制 CHANGELOG 对应版本的内容到描述框
6. 如果是 pre-release，勾选相应选项
7. 点击 "Publish release"

#### 6. 发布公告

- [ ] 在 GitHub Discussions 发布公告
- [ ] 更新相关社交媒体（如果有）
- [ ] 通知主要贡献者

## 紧急修复流程

对于紧急 bug 修复：

1. **创建 hotfix 分支**
   ```bash
   git checkout -b hotfix/critical-bug main
   ```

2. **修复并测试**
   - 快速定位问题
   - 实施最小化修复
   - 充分测试

3. **快速发布**
   ```bash
   git commit -m "fix: critical bug description"
   git checkout main
   git merge hotfix/critical-bug
   git tag -a v1.2.1 -m "Hotfix: critical bug"
   git push origin main --tags
   ```

4. **创建 GitHub Release**
   - 标注为 hotfix
   - 说明修复的问题
   - 建议用户尽快更新

## 社区管理

### 欢迎新贡献者

对于首次贡献者：
- 感谢他们的贡献
- 提供详细的代码审查反馈
- 引导他们了解项目规范
- 邀请他们继续参与

### 处理冲突

如遇社区冲突：
1. 保持冷静和专业
2. 参考 `CODE_OF_CONDUCT.md`
3. 公正处理
4. 必要时寻求其他维护者帮助

### 维护积极的社区氛围

- 及时回复 Issue 和 PR
- 鼓励积极参与
- 认可贡献者的工作
- 保持友好和包容

## 安全问题处理

### 收到安全报告时

1. **立即确认**
   - 24 小时内回复报告者
   - 感谢负责任的披露

2. **评估严重性**
   - 确定影响范围
   - 评估风险等级
   - 制定修复计划

3. **修复漏洞**
   - 创建私有分支
   - 实施修复
   - 充分测试

4. **发布补丁**
   - 尽快发布修复版本
   - 不要在发布前公开细节
   - 在 CHANGELOG 中提及（不要详细说明）

5. **公开披露**
   - 给用户时间更新
   - 发布安全公告
   - 感谢报告者

## 工具和自动化

### 推荐工具

- **GitHub CLI**: 命令行管理 GitHub
  ```bash
  gh pr list
  gh issue list
  gh release create
  ```

- **pre-commit**: 代码提交前检查
  ```bash
  pre-commit install
  pre-commit run --all-files
  ```

- **safety**: 依赖安全检查
  ```bash
  safety check
  ```

### 自动化脚本

可以创建脚本自动化常见任务：

```bash
# scripts/release.sh
#!/bin/bash
VERSION=$1
echo "Preparing release $VERSION"
# 更新 CHANGELOG
# 创建 tag
# 推送到 GitHub
```

## 备份和恢复

### 定期备份
- [ ] 配置文件
- [ ] 重要 Issue 和讨论
- [ ] 发布历史
- [ ] 文档快照

### 灾难恢复计划
- GitHub 账户访问凭证
- 备份维护者联系方式
- 项目恢复步骤文档

## 长期维护

### 定期审查（每季度）
- [ ] 审查未解决的 Issue
- [ ] 评估路线图进展
- [ ] 更新依赖
- [ ] 审查和更新文档
- [ ] 社区健康度检查

### 项目演进
- 收集用户反馈
- 评估新功能需求
- 考虑架构改进
- 保持与阿里云 API 同步

## 联系方式

维护者内部沟通：
- GitHub Discussions
- Issue 评论
- 私人邮件（紧急情况）

---

*本指南会根据项目发展持续更新。*
