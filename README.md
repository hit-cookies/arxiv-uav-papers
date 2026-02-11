# arXiv 无人机导航论文自动分析系统

[![GitHub Actions](https://github.com/USERNAME/REPO/workflows/arXiv%20Daily%20Paper%20Analysis/badge.svg)](https://github.com/USERNAME/REPO/actions)

每天自动获取 arXiv 上最新的无人机导航相关论文，使用 Google Gemini AI 分析论文的核心问题和创新点，并通过 Server 酱推送到微信。

## ✨ 功能特性

- 🔍 **自动获取论文**: 每天从 arXiv 获取最新的无人机导航相关论文
- ⭐ **优先机构筛选**: 优先展示来自 MIT、CMU、ETH、清华等顶尖研究机构的论文
- 🤖 **AI 智能分析**: 使用 Gemini AI 提取论文解决的问题和主要创新点
- 📱 **微信推送**: 通过 Server 酱将分析结果推送到微信
- ⏰ **定时运行**: 每天北京时间 10:00 自动执行

## 🏗️ 项目结构

```
.
├── .github/
│   └── workflows/
│       └── arxiv_daily.yml    # GitHub Actions 工作流配置
├── scripts/
│   ├── config.py              # 配置文件（研究机构列表、关键词等）
│   ├── fetch_papers.py        # 从 arXiv 获取论文
│   ├── analyze_papers.py      # 使用 Gemini AI 分析论文
│   ├── send_notification.py   # 通过 Server 酱发送通知
│   └── main.py                # 主执行脚本
├── requirements.txt           # Python 依赖
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 Fork 按钮，将项目复制到你的 GitHub 账号下。

### 2. 配置 GitHub Secrets

在你 Fork 的仓库中，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下两个 secrets：

#### `GEMINI_API_KEY`
- 获取方式：访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
- 示例值：`AIzaSyDUKTfijF5cU1sh4Z1slgpMGux776Q2PV0`

#### `SERVERCHAN_KEY`
- 获取方式：访问 [Server 酱官网](https://sct.ftqq.com/)，使用 GitHub 登录
- 示例值：`SCT314197TaQOHppVo3SJgbNvDZjhRXpRA`

### 3. 启用 GitHub Actions

1. 在你的仓库中，点击 `Actions` 标签页
2. 如果提示需要启用 workflows，点击 "I understand my workflows, go ahead and enable them"
3. 找到 "arXiv Daily Paper Analysis" workflow
4. 点击 "Enable workflow"

### 4. 测试运行

第一次可以手动触发测试：

1. 进入 `Actions` 标签页
2. 选择 "arXiv Daily Paper Analysis" workflow
3. 点击右侧 "Run workflow" 按钮
4. 点击绿色的 "Run workflow" 确认

等待几分钟后，检查你的微信是否收到推送消息。

## ⚙️ 配置说明

### 修改运行时间

编辑 [.github/workflows/arxiv_daily.yml](.github/workflows/arxiv_daily.yml)：

```yaml
schedule:
  - cron: '0 2 * * *'  # UTC 02:00 = 北京时间 10:00
```

### 修改优先研究机构

编辑 [scripts/config.py](scripts/config.py) 中的 `PRIORITY_INSTITUTIONS` 列表。

### 修改每日论文数量

编辑 [scripts/config.py](scripts/config.py) 中的 `MAX_PAPERS_PER_DAY` 参数（默认 20 篇）。

### 修改搜索关键词

编辑 [scripts/config.py](scripts/config.py) 中的 `SEARCH_KEYWORDS` 和 `NAVIGATION_KEYWORDS` 列表。

## 📊 费用说明

### Google Gemini API
- 模型：`gemini-1.5-flash`
- 定价：$0.075 / 1M tokens（输入）
- 估算：每天 20 篇论文约 $0.01-0.02
- 月费用：约 $0.30-0.60

### Server 酱
- 免费版：每天 5 条消息（本项目每天只发 1 条）
- 付费版：200 元/年，每天 1000 条消息

### GitHub Actions
- 公共仓库：完全免费，无限分钟数
- 私有仓库：每月 2000 分钟免费额度

**总计：每月约 ¥2-5**

## 🔍 论文搜索范围

### 关键词
- 无人机相关：UAV, drone, unmanned aerial vehicle, quadrotor
- 导航相关：navigation, path planning, trajectory, obstacle avoidance, SLAM

### arXiv 分类
- cs.RO (Robotics)
- cs.AI (Artificial Intelligence)
- cs.CV (Computer Vision)
- cs.LG (Machine Learning)

### 优先机构（部分）
- 北美：MIT, CMU, Stanford, UC Berkeley, UPenn
- 欧洲：ETH Zurich, TUM, Imperial College London
- 亚洲：清华大学, HKUST, NUS, 浙江大学, 北航

完整列表见 [scripts/config.py](scripts/config.py)。

## 🛠️ 本地测试

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export SERVERCHAN_KEY="your_serverchan_key"
```

### 运行脚本

```bash
cd scripts
python main.py
```

## 📝 示例输出

微信消息格式：

```
# 📚 今日 arXiv 无人机导航论文精选

**日期**: 2026年02月11日
**论文总数**: 15 篇
**优先机构**: 8 篇 ⭐
**AI分析成功**: 15/15 篇

---

### ⭐ 1. Deep Reinforcement Learning for Vision-based UAV Navigation

**作者**: Zhang Wei, Li Ming, Wang Hua 等
**发布日期**: 2024-02-10
**arXiv**: [2402.12345](https://arxiv.org/abs/2402.12345)

【解决的问题】
针对GPS拒止环境下无人机视觉导航的实时性和鲁棒性挑战

【主要创新点】
1. 提出了端到端的深度强化学习感知-规划框架
2. 设计了轻量级视觉特征提取网络适应嵌入式平台
3. 引入了不确定性感知的决策机制提高安全性

---

### 2. ...
```

## ❓ 常见问题

### Q: 为什么没有收到微信通知？

A: 检查以下几点：
1. 确认 `SERVERCHAN_KEY` 配置正确
2. 查看 GitHub Actions 运行日志是否有错误
3. Server 酱免费版每天限制 5 条消息

### Q: 如何关闭自动运行？

A: 在 GitHub Actions 页面，选择 workflow 后点击右上角 "..." → "Disable workflow"

### Q: 可以修改推送到企业微信吗？

A: 可以，修改 [scripts/send_notification.py](scripts/send_notification.py) 中的 `send_to_serverchan` 函数，改用企业微信机器人 webhook。

### Q: Gemini API 有免费额度吗？

A: 有免费层级，但有速率限制（gemini-1.5-flash: 15 RPM）。本项目已实现速率控制。

## 📜 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题，请提交 [Issue](https://github.com/USERNAME/REPO/issues)。
