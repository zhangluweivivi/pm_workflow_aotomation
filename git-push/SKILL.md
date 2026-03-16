---
name: git-push
description: |
  完整的 Git 仓库管理助手，支持仓库增删改查、文件级操作和回退撤销。
  使用 gh CLI 和 git 命令管理 GitHub 仓库。
  
  使用场景：
  1. Skill开发版本管理
  2. 配置文件同步
  3. 代码版本控制
  4. 团队协作开发
  
  触发关键词：git推送、新建仓库、删除分支、回退提交、查看状态
license: MIT
compatibility: |
  需要 git 和 gh (GitHub CLI) 已安装。
  支持 Ubuntu/Debian 和 macOS 系统。
metadata:
  version: "2.1.0"
  author: zhangluweivivi
  homepage: https://github.com/zhangluweivivi/pm_workflow_aotomation
  requires:
    bins:
      - git
      - gh
---

# git-push

完整的 Git 仓库管理助手，支持仓库增删改查、文件级操作和回退撤销。

## When to Use

触发此 skill 当用户：
- 需要将代码推送到 GitHub
- 想要新建 GitHub 仓库
- 需要删除分支或文件
- 想要回退/撤销提交
- 需要查看仓库状态或历史
- 遇到推送冲突需要解决

## Quick Start

### 新建仓库并推送
```bash
gh repo create my-repo --private --source=. --push
```

### 标准推送流程
```bash
git add -A
git commit -m "update"
git push origin main
```

### 删除远程分支
```bash
git push origin --delete branch-name
```

### 回退到上一版本
```bash
git reset --soft HEAD~1
```

### 查看状态
```bash
git status
git log --oneline -10
```

## Workflow

### 【增】新建与添加

#### 新建 GitHub 仓库
```bash
# 方式1：使用 GitHub CLI（推荐）
gh repo create <repo-name> --private --source=. --push

# 方式2：使用 API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"<repo>","private":true}'
```

#### 添加文件到仓库
```bash
git add <files>
git commit -m "feat: add new feature"
git push origin main
```

### 【删】删除仓库/文件/分支

#### 删除整个仓库（⚠️危险）
```bash
gh repo delete <owner>/<repo> --confirm
```

#### 删除分支
```bash
# 删除远程分支
git push origin --delete <branch-name>

# 删除本地分支
git branch -d <branch-name>
```

#### 删除文件/目录
```bash
git rm -r <directory>
git commit -m "remove: delete files"
git push
```

### 【改】更新推送

#### 标准推送
```bash
git add -A
git commit -m "update message"
git push origin main
```

#### 处理冲突
```bash
# 拉取并合并
git pull origin main --no-rebase
# 解决冲突后
git push origin main
```

### 【查】查询状态

```bash
# 查看工作状态
git status

# 查看提交历史
git log --oneline -10

# 查看分支
git branch -a

# 查看远程信息
git remote -v
```

### 【回】回退与撤销

#### 回退推送（删除远程分支）
```bash
git push origin --delete <branch-name>
```

#### 回退到上一版本
```bash
# 软回退（保留修改）
git reset --soft HEAD~1

# 混合回退（保留修改到工作区）
git reset --mixed HEAD~1

# 硬回退（完全丢弃）
git reset --hard HEAD~1
```

#### 安全撤销已推送提交
```bash
git revert <commit-hash>
git push
```

## Examples

### Example 1: 新建仓库
用户："新建仓库 git-push-skill"

系统：
1. 确认仓库名称和隐私设置
2. 检查本地目录
3. 执行 `gh repo create`
4. 返回新仓库 URL

### Example 2: 回退推送
用户："回退刚才的推送"

系统：
1. 查询最近操作历史
2. 确认回退范围
3. 提供回退选项（删除分支/强制回滚/revert）
4. 执行并返回结果

### Example 3: 解决冲突
用户："推送失败了，说有冲突"

系统：
1. 执行 `git pull origin main --no-rebase`
2. 指导用户解决冲突
3. 重新推送

## Notes

- 使用 `--force` 需谨慎，可能导致数据丢失
- 删除仓库操作不可恢复，会二次确认
- 建议配置 SSH 密钥避免重复输入密码

## Version History

- **v2.1.0** (2026-03-13): 新增回退操作、删除文件功能、操作历史记录
- **v2.0.0** (2026-03-13): 新增增删改查四种操作模式、交互式询问流程
- **v1.0.0** (2026-03-13): 初始版本，支持自动推送和SSH配置
