---
name: git-push
description: "完整的 Git 仓库管理助手，支持仓库增删改查、文件级操作和回退撤销。使用 gh CLI 和 git 命令管理 GitHub 仓库。"
metadata: {"clawdbot":{"requires":{"bins":["git","gh"]},"install":[{"id":"git","kind":"apt","package":"git","bins":["git"],"label":"Install Git"},{"id":"gh","kind":"apt","package":"gh","bins":["gh"],"label":"Install GitHub CLI"}]}}
---

# Git Push Skill v2.1

完整的 Git 仓库管理助手，支持仓库增删改查、文件级操作和回退撤销。

## 功能特性

### 🔧 五大操作模式

| 模式 | 功能 | 示例命令 |
|-----|------|---------|
| **增** | 新建仓库、添加文件 | `gh repo create` / `git add` |
| **删** | 删除仓库、删除文件/分支 | `gh repo delete` / `git rm` |
| **改** | 更新推送、修改文件 | `git commit` / `git push` |
| **查** | 查询状态、查看历史 | `git status` / `git log` |
| **回** | 回退操作、撤销推送 | `git reset` / `git revert` |

### 🔑 核心能力
- SSH密钥生成与配置
- GitHub API 集成（创建/删除仓库）
- 智能冲突检测与合并
- 操作历史记录与回退
- 推送状态报告

## 使用场景
- Skill开发版本管理
- 配置文件同步
- 代码版本控制
- 团队协作开发

---

## 快速使用

### 新建仓库
```bash
# 创建新仓库并推送
gh repo create my-repo --private --source=. --push
```

### 更新推送
```bash
# 标准推送流程
git add -A
git commit -m "update"
git push origin main
```

### 删除分支
```bash
# 删除远程分支
git push origin --delete branch-name

# 删除本地分支
git branch -d branch-name
```

### 回退操作
```bash
# 删除远程分支（回退推送）
git push origin --delete branch-name

# 回退到上一版本
git reset --soft HEAD~1

# 安全撤销已推送提交
git revert <commit-hash>
```

### 查询状态
```bash
# 查看完整状态
git status
git log --oneline -10
git branch -a
```

---

## 详细指南

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

---

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

---

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

---

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

---

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

---

## 交互式使用场景

### 场景1：新建仓库
**用户**: "新建仓库 git-push-skill"

**系统交互**:
1. 询问："仓库名称: git-push-skill，是否私有？(y/n)"
2. 询问："本地目录: /path/to/git-push-skill"
3. 询问："是否初始化 README？(y/n)"
4. 执行并返回新仓库 URL

### 场景2：回退操作
**用户**: "回退刚才的推送"

**系统交互**:
1. 查询最近操作历史
2. 确认："回退刚才推送到 skills-subtree 的操作？"
3. 询问回退方式：
   - a) 删除远程分支（完全移除）
   - b) 强制回滚到上一版本
   - c) revert（生成反向提交）
4. 执行并返回结果

---

## 依赖安装

### Git
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git
```

### GitHub CLI
```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo apt-get install gh

# macOS
brew install gh
```

### SSH 配置
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your@email.com"

# 添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 复制到 GitHub Settings -> SSH Keys
```

---

## 版本历史

- **v2.1.0** (2026-03-13): 新增回退操作、删除文件功能、操作历史记录
- **v2.0.0** (2026-03-13): 新增增删改查四种操作模式、交互式询问流程
- **v1.0.0** (2026-03-13): 初始版本，支持自动推送和SSH配置
