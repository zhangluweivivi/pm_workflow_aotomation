#!/bin/bash
# Git Push Skill - 新建仓库脚本
# 用法: ./create-repo.sh <仓库名> [--public|--private]

REPO_NAME=$1
VISIBILITY=${2:---private}

if [ -z "$REPO_NAME" ]; then
    echo "❌ 错误: 请提供仓库名"
    echo "用法: ./create-repo.sh my-repo [--public|--private]"
    exit 1
fi

echo "🔨 创建仓库: $REPO_NAME"
echo "📦 可见性: $VISIBILITY"
echo ""

# 使用 gh CLI 创建仓库
gh repo create "$REPO_NAME" $VISIBILITY --source=. --remote=origin --push

echo ""
echo "✅ 仓库创建完成!"
echo "🌐 访问: https://github.com/$(gh api user -q '.login')/$REPO_NAME"
