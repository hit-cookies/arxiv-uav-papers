#!/bin/bash

# arXiv 无人机论文系统 - 快速部署脚本

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     arXiv 无人机导航论文自动分析系统 - 部署助手            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在项目目录中
if [ ! -f "requirements.txt" ] || [ ! -d "scripts" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 1. 初始化 git
echo "📦 初始化 Git 仓库..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git 仓库初始化完成"
else
    echo "⚠️  Git 仓库已存在，跳过初始化"
fi

# 2. 添加文件
echo ""
echo "📝 添加文件到 Git..."
git add .
git status --short
echo "✅ 文件添加完成"

# 3. 提交
echo ""
echo "💾 创建初始提交..."
git commit -m "初始提交: arXiv 无人机导航论文自动分析系统" || echo "⚠️  可能已经提交过了"

# 4. 询问 GitHub 仓库地址
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "请完成以下步骤："
echo "1. 访问 https://github.com/new 创建新仓库"
echo "2. 仓库名称建议: arxiv-uav-paper-analysis"
echo "3. 设置为 Public (免费Actions分钟数)"
echo "4. 不要勾选 'Initialize with README'"
echo "5. 创建后复制仓库 URL"
echo "═══════════════════════════════════════════════════════════"
echo ""
read -p "请输入你的 GitHub 仓库 URL (例如: https://github.com/username/repo.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 未输入仓库 URL，退出"
    exit 1
fi

# 5. 添加远程仓库
echo ""
echo "🔗 添加远程仓库..."
git remote remove origin 2>/dev/null
git remote add origin "$REPO_URL"
echo "✅ 远程仓库已配置"

# 6. 推送代码
echo ""
echo "🚀 推送代码到 GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              ✅ 代码推送成功！                             ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "📌 下一步操作："
    echo ""
    echo "1️⃣  配置 GitHub Secrets:"
    echo "   - 访问你的仓库 Settings → Secrets and variables → Actions"
    echo "   - 添加 GEMINI_API_KEY (你的 Gemini API key)"
    echo "   - 添加 SERVERCHAN_KEY: SCT314197TaQOHppVo3SJgbNvDZjhRXpRA"
    echo ""
    echo "2️⃣  启用 GitHub Actions:"
    echo "   - 进入仓库的 Actions 标签页"
    echo "   - 点击 'I understand my workflows, go ahead and enable them'"
    echo ""
    echo "3️⃣  手动测试运行:"
    echo "   - 在 Actions 页面选择 'arXiv Daily Paper Analysis'"
    echo "   - 点击 'Run workflow' 按钮"
    echo "   - 等待运行完成并检查微信消息"
    echo ""
    echo "📖 详细说明请查看 DEPLOY.md 文件"
    echo ""
else
    echo ""
    echo "❌ 推送失败，可能需要:"
    echo "1. 检查 GitHub 仓库是否已创建"
    echo "2. 检查 Git 认证配置"
    echo "3. 手动运行: git push -u origin main"
    echo ""
fi
