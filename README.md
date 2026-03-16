# PM Workflow Automation

产品经理工作流自动化工具集 - OpenClaw Agent Skills

## 📦 包含 Skills

### 1. git-push
完整的 Git 仓库管理助手，支持仓库增删改查、文件级操作和回退撤销。

**功能特性:**
- 🔧 五大操作模式：增/删/改/查/回
- 🔑 SSH密钥生成与配置
- 🚀 自动commit和push
- 🔄 智能冲突检测与合并
- ⏪ 操作回退与撤销

**快速使用:**
```bash
# 推送到当前仓库
cd skills/git-push
./scripts/push.sh

# 新建仓库
./scripts/create-repo.sh my-new-repo --private

# 回退操作
./scripts/rollback.sh --delete-branch branch-name
```

### 2. brainstorm
结构化头脑风暴助手，通过多维度引导激发创意。

**功能特性:**
- 💡 5维度创意激发（技术/用户/商业/创新/成本）
- 📝 结构化思维导图
- 🎯 可行性评估
- 📋 行动项提取

---

## 🚀 快速开始

### 环境要求
- Git >= 2.30
- GitHub CLI >= 2.0
- Bash >= 4.0

### 安装

```bash
# 1. 克隆仓库
git clone git@github.com:zhangluweivivi/pm_workflow_aotomation.git
cd pm_workflow_aotomation

# 2. 安装依赖（GitHub CLI）
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# macOS
brew install gh

# 3. 配置 GitHub CLI
gh auth login
```

### 使用 Skills

#### git-push
```bash
cd skills/git-push

# 查看帮助
cat SKILL.md

# 执行推送
./scripts/push.sh

# 新建仓库
./scripts/create-repo.sh my-repo --private
```


## 📁 目录结构

```
pm_workflow_aotomation/
├── README.md                    # 本文件
├── LICENSE                      # MIT 许可证
├── skills/
│   ├── git-push/               # Git 管理 Skill
│   │   ├── SKILL.md            # 技能文档
│   │   ├── _meta.json          # 元数据
│   │   └── scripts/            # 执行脚本
│   │       ├── push.sh
│   │       ├── create-repo.sh
│   │       └── rollback.sh
└── docs/                       # 文档目录
    └── usage-guide.md
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📧 联系

- GitHub: [@zhangluweivivi](https://github.com/zhangluweivivi)
- 项目主页: https://github.com/zhangluweivivi/pm_workflow_aotomation
