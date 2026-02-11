# 🚀 部署指南

## 项目状态

✅ **代码已完成** - 所有模块已实现并测试
⚠️ **需要配置 API keys** - Gemini API key 已超出免费配额

---

## 📋 部署步骤

### 1. 获取新的 Gemini API Key

你当前的 API key (`AIzaSyDUKTfijF5cU1sh4Z1slgpMGux776Q2PV0`) 已超出免费额度。

**获取新 API Key:**
1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用 Google 账号登录
3. 点击 "Get API key" 或 "Create API key"
4. 复制新生成的 API key

**免费额度说明:**
- 模型: `gemini-pro-latest`
- 免费层级每天有请求限制
- 每分钟 15 次请求（RPM）
- 建议: 如果免费额度不够，可以开通付费账户

---

### 2. 验证 Server 酱配置

你的 SendKey: `SCT314197TaQOHppVo3SJgbNvDZjhRXpRA`

**验证步骤:**
1. 访问 https://sct.ftqq.com/
2. 检查 SendKey 是否正确
3. 确认已绑定微信为接收消息

> **注意:** 本地测试时遇到 SSL 连接问题是网络环境导致的，GitHub Actions 环境中不会有此问题。

---

### 3. 上传代码到 GitHub

#### 初始化 Git 仓库

```bash
cd /media/k311-ytd/F1EBC32ABB6B8A7D/github_action

# 初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始提交: arXiv 无人机导航论文自动分析系统"
```

#### 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称: `arxiv-uav-paper-analysis` (或你喜欢的名字)
3. 设置为 **Public** (免费 GitHub Actions 分钟数)
4. **不要**勾选 "Initialize with README" (我们已有 README)
5. 点击 "Create repository"

#### 推送代码

```bash
# 添加远程仓库 (替换 YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/arxiv-uav-paper-analysis.git

# 推送代码
git branch -M main
git push -u origin main
```

---

### 4. 配置 GitHub Secrets

在你的 GitHub 仓库中：

1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 点击 "New repository secret"

#### 添加 GEMINI_API_KEY
- Name: `GEMINI_API_KEY`
- Secret: `你的新 Gemini API key`
- 点击 "Add secret"

#### 添加 SERVERCHAN_KEY
- Name: `SERVERCHAN_KEY`
- Secret: `SCT314197TaQOHppVo3SJgbNvDZjhRXpRA`
- 点击 "Add secret"

---

### 5. 启用并测试 GitHub Actions

#### 启用 Workflow

1. 进入仓库的 `Actions` 标签页
2. 如果显示 "Workflows aren't being run..."，点击 "I understand my workflows, go ahead and enable them"
3. 找到 "arXiv Daily Paper Analysis" workflow

#### 手动触发测试

1. 点击 "arXiv Daily Paper Analysis" workflow
2. 点击右侧 "Run workflow" 下拉菜单
3. 选择 main 分支
4. 点击绿色的 "Run workflow" 按钮
5. 等待几分钟，查看运行状态

#### 查看运行日志

1. 点击正在运行的 workflow
2. 点击 "fetch-and-analyze" job
3. 展开各个步骤查看详细日志

---

### 6. 验证结果

#### 成功标志:
- ✅ GitHub Actions 运行状态为绿色勾
- ✅ 微信收到推送消息
- ✅ 消息包含论文标题、作者、问题和创新点

#### 如果失败:
1. 查看 GitHub Actions 运行日志中的错误信息
2. 常见问题:
   - Gemini API key 无效或超额 → 更换新 key
   - Server 酱推送失败 → 检查 SendKey 是否正确
   - arXiv API 查询无结果 → 正常，可能当天没有相关论文

---

## ⏰ 自动运行时间

系统会在每天 **北京时间上午 10:00** 自动运行（UTC 02:00）。

修改运行时间：编辑 `.github/workflows/arxiv_daily.yml`:

```yaml
schedule:
  - cron: '0 2 * * *'  # UTC time
```

转换工具: https://crontab.guru/

---

## 🔧 常见问题

### Q: 如何修改每天论文数量？
A: 编辑 `scripts/config.py` 中的 `MAX_PAPERS_PER_DAY`

### Q: 如何添加更多优先研究机构？
A: 编辑 `scripts/config.py` 中的 `PRIORITY_INSTITUTIONS` 列表

### Q: 如何修改搜索关键词？
A: 编辑 `scripts/config.py` 中的 `SEARCH_KEYWORDS` 和 `NAVIGATION_KEYWORDS`

### Q: Server 酱免费版每天只有5条消息，够用吗？
A: 够用！系统每天只发送 1 条合并消息（包含所有论文）

### Q: Gemini API 免费额度是多少？
A: 免费层级：每天约 1500 次请求，每分钟 15 次请求。处理 20 篇论文足够。

---

## 📞 获取帮助

如果遇到问题：
1. 查看 [README.md](README.md) 了解系统说明
2. 查看 GitHub Actions 运行日志
3. 提交 Issue 到 GitHub 仓库

---

## ✅ 快速检查清单

部署前确认：

- [ ] 获取了新的 Gemini API key
- [ ] Server 酱 SendKey 已验证
- [ ] 代码已上传到 GitHub
- [ ] GitHub Secrets 已正确配置
- [ ] GitHub Actions 已启用
- [ ] 手动触发测试通过
- [ ] 微信收到测试消息

---

**祝你使用愉快！** 🎉

每天早上 10 点准时收到最新的无人机导航论文分析！
