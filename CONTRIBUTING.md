# 贡献指南

首先，感谢你愿意为 aliyun-update-security-ips 项目做出贡献！ 🎉

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请创建一个 Issue，并包含以下信息：

- 清晰的标题和描述
- 重现步骤
- 期望行为
- 实际行为
- 你的环境信息（操作系统、Python 版本等）
- 如果可能，提供相关的日志或截图

### 提出新功能

如果你有好的想法，欢迎创建一个 Issue 来讨论：

- 描述你想要的功能
- 解释为什么需要这个功能
- 如果可能，提供一些实现思路

### 提交代码

1. **Fork 项目**
   
   点击右上角的 Fork 按钮，将项目 fork 到你的账号下。

2. **克隆仓库**
   
   ```bash
   git clone https://github.com/your-username/aliyun-update-security-ips.git
   cd aliyun-update-security-ips
   ```

3. **创建分支**
   
   ```bash
   git checkout -b feature/your-feature-name
   ```
   
   分支命名规范：
   - 新功能：`feature/功能名称`
   - Bug 修复：`fix/bug描述`
   - 文档更新：`docs/文档描述`

4. **进行修改**
   
   - 保持代码风格一致
   - 添加必要的注释
   - 如果添加新功能，请更新文档

5. **提交代码**
   
   ```bash
   git add .
   git commit -m "描述你的修改"
   ```
   
   Commit 信息格式：
   - `feat: 添加新功能`
   - `fix: 修复问题`
   - `docs: 更新文档`
   - `style: 代码格式调整`
   - `refactor: 代码重构`
   - `test: 添加测试`

6. **推送到 GitHub**
   
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   
   - 在 GitHub 上创建 Pull Request
   - 清晰地描述你的修改
   - 关联相关的 Issue

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 风格指南
- 使用 4 个空格缩进
- 行长度不超过 120 字符
- 使用有意义的变量名和函数名

### 文档

- 所有公共函数和类都应该有文档字符串
- README 应该保持更新
- 注释应该解释"为什么"而不只是"是什么"

## 开发环境设置

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境：
   ```bash
   cp .env.example .env
   cp config.example.yml config.yml
   ```

3. 编辑配置文件，填入你的测试凭证

## 测试

在提交 PR 之前，请确保：

- 代码能够正常运行
- 没有引入新的 bug
- 如果可能，添加相应的测试用例

## 问题？

如果你有任何问题，可以：

- 创建 Issue 询问
- 在 PR 中讨论
- 通过项目主页联系维护者

再次感谢你的贡献！ ❤️
