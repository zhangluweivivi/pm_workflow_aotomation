---
name: xiaohongshu-get-idea
description: |
  小红书爆款内容分析与创意提取工具。自动下载小红书笔记（图文/视频），提取关键帧和音频，
  分析视觉风格、听觉特征、复刻可行性，并生成 AI 反推提示词。
  
  使用场景：
  1. 用户发送小红书笔记链接，要求分析/拆解/学习这个内容
  2. 用户说"帮我看看这个为什么火"
  3. 用户想复刻某个爆款视频/图文
  4. 用户需要提取小红书内容的创意元素
  
  触发关键词：小红书分析、拆解笔记、提取创意、为什么数据好、复刻这个、学习这个爆款
---

# 小红书创意提取助手

帮助用户深度分析小红书爆款内容，提取可复刻的创意元素。

## 工作流程

### 1. 解析笔记链接

从小红书分享链接中提取 `feed_id` 和 `xsec_token`：
- URL 格式: `https://www.xiaohongshu.com/explore/{feed_id}?xsec_token={token}`
- 从 URL 参数中提取这两个值

### 2. 获取笔记详情

使用 xiaohongshu-skills 的 CDP 工具获取笔记数据：

```bash
cd /Users/zlw/clawd/agents-skills-personal/xiaohongshu-skills-main
uv run python scripts/cli.py get-feed-detail \
  --feed-id {feed_id} \
  --xsec-token {xsec_token}
```

### 3. 下载媒体内容

#### 图文笔记
- 从 `imageList` 提取所有图片 URL
- 下载到本地分析目录

#### 视频笔记
- 从 `video` 或 `videoList` 提取视频 URL
- 下载视频文件
- 使用 ffmpeg 提取关键帧（每 5-10 秒一帧）
- 提取音频为 WAV 格式

```bash
# 下载视频
curl -L -o video.mp4 "{video_url}"

# 提取关键帧（每10秒）
mkdir -p frames
ffmpeg -i video.mp4 -vf "fps=1/10,scale=720:-1" -q:v 2 frames/frame_%03d.jpg

# 提取音频
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 audio.wav
```

### 4. 内容分析维度

#### 数据分析
- 点赞数、收藏数、评论数
- 互动率估算（点赞/收藏比）
- 发布时间、标签

#### 视觉分析（图文/视频帧）
- **配色方案**：主色调、渐变、对比度
- **构图风格**：对称、三分法、中心聚焦
- **视觉元素**：主体类型、装饰元素、文字排版
- **风格标签**：极简、复古、赛博朋克、治愈系等

#### 听觉分析（视频）
- **音乐类型**：电子、流行、古典、氛围音乐
- **节奏特征**：BPM、节拍型
- **情绪标签**：治愈、激励、神秘、放松

#### 文案分析
- 标题结构
- 正文风格
- 标签策略
- 评论区热点

### 5. 复刻可行性评估

| 维度 | 难度评级 | AI/工具方案 |
|------|---------|------------|
| 视觉复刻 | ⭐-⭐⭐⭐ | Midjourney/SD/即梦、Blender、Canva |
| 音乐复刻 | ⭐-⭐⭐ | Suno/Udio/Stable Audio |
| 文案复刻 | ⭐ | Claude/ChatGPT |
| 整体制作 | ⭐⭐-⭐⭐⭐⭐ | 剪映/CapCut + AI 工具组合 |

### 6. 生成 AI 反推提示词

**重要：基于实际关键帧画面内容生成具体提示词，不是通用模板**

分析步骤：
1. 仔细观察所有关键帧图片的实际画面内容
2. 识别具体的主体、配色、光影、构图、动作
3. 基于实际观察生成具体的、可复刻的提示词

#### 图像生成提示词（Midjourney/SD/即梦）

基于实际画面生成3-5个具体场景的提示词：

**首帧/封面画面：**
```
[基于实际首帧画面的具体描述，如：主体类型、颜色、位置、光线、背景]
[风格关键词]
[技术参数：--ar 9:16 --v 6]
```

**关键动作画面：**
```
[基于实际动作帧的具体描述，如：手部动作、物体交互、光影变化]
[氛围关键词]
[技术参数]
```

**氛围/场景画面：**
```
[基于实际场景帧的具体描述，如：环境、光线、情绪]
[风格关键词]
[技术参数]
```

#### 视频生成提示词（可灵/Runway/Pika）

```
Scene: [具体场景描述，基于实际画面]
Lighting: [具体光线描述，基于实际光影]
Camera: [运镜方式，基于实际视频节奏]
Action: [具体动作描述，基于实际关键帧变化]
Duration: [建议时长]
Style: [具体风格标签]
Mood: [具体情绪关键词]
```

#### 音乐/声音生成提示词（Suno/Udio）

```
Style: [基于实际音频的具体音乐类型]
Sounds: [具体声音元素描述]
Environment: [环境音特征]
Tempo: [基于实际音频的BPM或节奏特征]
[如果是ASMR：具体ASMR触发器类型]
Duration: [时长]
Mood: [基于实际音频的情绪标签]
```

#### 拍摄/制作参数表

| 元素 | 具体参数（基于实际内容） |
|-----|------------------------|
| 光源 | [具体光源类型、位置、数量] |
| 背景 | [具体背景描述] |
| 相机设置 | [基于画面质量的推测参数] |
| 色调 | [具体主色、辅助色] |
| 构图 | [具体构图方式] |
| 动作 | [具体动作描述] |
| 音频 | [具体音频特征] |

### 7. 输出格式

生成结构化分析报告：

```markdown
## 📊 数据表现
- 点赞: X万 | 收藏: X万 | 评论: X
- 互动率: XX%
- 标签: #xxx #xxx

## 🎨 视觉分析
- 风格: xxx
- 配色: xxx
- 构图: xxx
- 关键元素: xxx

## 🎵 听觉分析（如适用）
- 类型: xxx
- 节奏: xxx BPM
- 情绪: xxx

## ✅ 复刻难度: X/5
| 元素 | 难度 | 工具 |
|-----|-----|-----|
| ... | ... | ... |

## 🚀 AI 反推提示词

### 图像/视频
```
...
```

### 音乐（如适用）
```
...
```

## 💡 为什么数据好？
1. ...
2. ...
3. ...
```

## 快速使用

### 一键分析

```bash
cd /Users/zlw/clawd/agents-skills-personal/xiaohongshu_get_idea
python3 scripts/analyze.py "小红书链接" -o ./output
```

### 分步执行

```bash
# 1. 下载笔记内容
python3 scripts/download_and_extract.py "小红书链接" -o ./output

# 2. 生成 AI 分析提示词
python3 scripts/generate_prompt.py ./output/metadata.json -o ./output/prompt.txt
```

### 与 AI 配合分析

1. 运行分析脚本获取笔记数据和关键帧
2. 读取 `analysis_prompt.txt` 中的提示词
3. 将提示词 + 关键帧图片发送给 AI（Claude/GPT）
4. AI 输出完整的分析报告和反推提示词

## 依赖要求

- 已安装 xiaohongshu-skills: `/Users/zlw/clawd/agents-skills-personal/xiaohongshu-skills-main`
- 已安装 ffmpeg
- 已安装 uv (Python 包管理器)
- Chrome 浏览器（用于 CDP 自动化）

## 故障排除

**无法获取笔记详情**
- 检查 feed_id 和 xsec_token 是否正确
- 确认 Chrome 已启动: `uv run python scripts/chrome_launcher.py`
- 检查是否需要登录: `uv run python scripts/cli.py check-login`

**视频下载失败**
- 小红书视频 URL 有时效性，需要尽快下载
- 如果失败，尝试重新获取笔记详情获取新的 URL

**ffmpeg 命令失败**
- 检查 ffmpeg 是否安装: `ffmpeg -version`
- 确保输出目录存在: `mkdir -p frames`
