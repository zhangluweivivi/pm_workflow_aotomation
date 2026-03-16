---
name: xiaohongshu-get-idea
version: 1.0.0
description: |
  小红书爆款内容分析与创意提取工具。自动分析小红书笔记链接，提取关键信息，
  生成可复刻的创意元素和 AI 反推提示词。
  
  使用场景：
  1. 用户发送小红书笔记链接，要求分析/拆解/学习这个内容
  2. 用户说"帮我看看这个为什么火"
  3. 用户想复刻某个爆款视频/图文
  4. 用户需要提取小红书内容的创意元素
  
  触发关键词：小红书分析、拆解笔记、提取创意、为什么数据好、复刻这个、学习这个爆款
metadata:
  requires:
    bins:
      - python3
      - ffmpeg
    skills:
      - xiaohongshu-explore
homepage: https://github.com/zhangluweivivi/pm_workflow_aotomation
---

# xiaohongshu-get-idea

小红书爆款内容分析与创意提取工具。

## When to Use

触发此 skill 当用户：
- 发送小红书笔记链接并要求分析
- 询问"为什么这个内容火"
- 想要"复刻"某个爆款
- 需要提取创意元素用于创作
- 想了解爆款内容的制作技巧

## Quick Start

### 分析小红书笔记

用户提供小红书链接后，自动执行：

```python
# Step 1: 提取笔记信息
web_fetch(url="https://www.xiaohongshu.com/explore/xxx")

# Step 2: 获取笔记详情（需要 xiaohongshu-explore skill）
# 调用 xiaohongshu-explore 的 get-note 功能

# Step 3: 分析并生成报告
# 使用AI分析提取的数据
```

## Workflow

### Step 1: 解析笔记链接

从用户提供的小红书链接中提取信息：
- URL 格式: `https://www.xiaohongshu.com/explore/{feed_id}?xsec_token={token}`
- 提取 `feed_id` 和 `xsec_token`

### Step 2: 获取笔记详情

使用 xiaohongshu-explore skill 获取笔记数据：

```python
# 使用 xiaohongshu-explore skill 获取笔记详情
exec(command="python3 -m xiaohongshu_explore get-note --url {user_url}")
```

### Step 3: 数据分析维度

获取数据后分析以下维度：

#### 数据表现
- 点赞数、收藏数、评论数
- 互动率估算
- 发布时间、标签

#### 内容分析
- **视觉风格**：配色、构图、视觉元素
- **文案结构**：标题、正文、标签策略
- **情绪价值**：给用户带来的情感体验

#### 复刻可行性
| 维度 | 难度评级 | AI/工具方案 |
|------|---------|------------|
| 视觉复刻 | ⭐-⭐⭐⭐ | Midjourney/SD/即梦 |
| 文案复刻 | ⭐ | Claude/ChatGPT |
| 整体制作 | ⭐⭐-⭐⭐⭐⭐ | 剪映/CapCut + AI |

### Step 4: 生成 AI 反推提示词

基于分析结果生成：

1. **图像生成提示词**（Midjourney/SD/即梦）
2. **视频生成提示词**（可灵/Runway）
3. **文案结构模板**

## Output Format

生成结构化分析报告：

```markdown
## 📊 数据表现
- 点赞: X万 | 收藏: X万 | 评论: X
- 标签: #xxx #xxx

## 🎨 内容分析
- 风格: xxx
- 配色: xxx
- 文案结构: xxx
- 情绪价值: xxx

## ✅ 复刻难度: X/5
| 元素 | 难度 | 工具 |
|-----|-----|-----|
| ... | ... | ... |

## 🚀 AI 反推提示词

### 图像/视频
```
...
```

### 文案结构
```
...
```

## 💡 为什么数据好？
1. ...
2. ...
3. ...
```

## Dependencies

此 skill 依赖以下工具：

### 必需
- `python3` - 执行分析脚本
- `xiaohongshu-explore` skill - 获取小红书笔记数据

### 可选（用于完整分析）
- `ffmpeg` - 视频关键帧提取

## Examples

### Example 1: 分析图文笔记
用户："帮我分析这个小红书笔记 https://www.xiaohongshu.com/explore/abc123"

系统：
1. 提取 feed_id 和 xsec_token
2. 调用 xiaohongshu-explore 获取笔记详情
3. 分析数据表现和内容特征
4. 生成复刻建议和 AI 提示词
5. 输出完整分析报告

### Example 2: 学习爆款技巧
用户："为什么这个视频这么火？"

系统：
1. 获取笔记数据
2. 分析视觉风格、文案技巧、情绪价值
3. 总结爆款原因
4. 提供可复用的创作技巧

## Notes

- 小红书视频 URL 有时效性，需尽快分析
- 部分笔记可能需要登录才能查看完整数据
- 分析结果基于公开可见的信息

## Version History

- **v1.0.0** (2026-03-16): 初始版本，支持笔记分析和创意提取
