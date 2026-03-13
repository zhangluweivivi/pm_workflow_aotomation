#!/bin/bash
# Git Push Skill - 回退操作脚本
# 用法: ./rollback.sh [--delete-branch <分支名>] [--reset <模式>] [--revert <commit>]

MODE=$1
TARGET=$2

case $MODE in
    --delete-branch)
        echo "🗑️  删除远程分支: $TARGET"
        git push origin --delete "$TARGET"
        echo "✅ 分支已删除"
        ;;
    --reset)
        MODE_TYPE=${TARGET:-soft}
        echo "⏪ 回退到上一版本 (模式: $MODE_TYPE)"
        git reset --$MODE_TYPE HEAD~1
        echo "✅ 已回退"
        ;;
    --revert)
        echo "↩️  撤销提交: $TARGET"
        git revert "$TARGET" --no-edit
        git push
        echo "✅ 已生成 revert 提交"
        ;;
    *)
        echo "用法:"
        echo "  ./rollback.sh --delete-branch <分支名>  # 删除远程分支"
        echo "  ./rollback.sh --reset [soft|mixed|hard]  # 回退到上一版本"
        echo "  ./rollback.sh --revert <commit-hash>     # 撤销指定提交"
        exit 1
        ;;
esac
