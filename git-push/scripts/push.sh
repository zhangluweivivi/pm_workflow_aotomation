#!/bin/bash
# Git Push Skill - 快速推送脚本
# 用法: ./push.sh [仓库路径] [提交信息]

REPO_PATH=${1:-"."}
COMMIT_MSG=${2:-"update: $(date '+%Y-%m-%d %H:%M')"}

cd "$REPO_PATH" || exit 1

echo "📁 当前目录: $(pwd)"
echo ""

# 检查 git 状态
echo "📊 Git 状态:"
git status --short

# 检查是否有变更
if [ -z "$(git status --short)" ]; then
    echo ""
    echo "✅ 没有变更需要提交"
    exit 0
fi

echo ""
echo "📝 添加变更..."
git add -A

echo ""
echo "💾 提交变更..."
git commit -m "$COMMIT_MSG"

echo ""
echo "🚀 推送到远程..."
git push origin $(git branch --show-current)

echo ""
echo "✅ 推送完成!"
