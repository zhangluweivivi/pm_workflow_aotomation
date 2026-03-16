#!/usr/bin/env python3
"""
生成 AI 分析提示词
根据笔记元数据生成结构化的分析框架和具体反推提示词
"""

import argparse
import json
from pathlib import Path


def generate_analysis_prompt(metadata: dict, has_frames: bool, has_audio: bool) -> str:
    """生成 AI 分析提示词"""
    
    content_type = "视频" if metadata.get("has_video") else "图文"
    duration_str = metadata.get("video_duration_formatted", "")
    duration_line = f"- 视频时长: {duration_str}" if duration_str else ""
    
    prompt = f"""## 笔记基础信息
- 标题: {metadata.get('title') or '(无标题)'}
- 作者: {metadata.get('author', {}).get('nickname', '')}
- 类型: {content_type}
- 点赞: {metadata.get('stats', {}).get('likes', '0')}
- 收藏: {metadata.get('stats', {}).get('collects', '0')}
- 评论: {metadata.get('stats', {}).get('comments', '0')}
- 标签: {', '.join(metadata.get('tags', []))}
- 描述: {metadata.get('description', '') or '(无文字描述)'}
{duration_line}

## 视觉分析参考（基于关键帧）

### 整体视觉风格
[基于所有关键帧的整体风格判断：极简/复古/赛博朋克/治愈系/科技感/暗调美学等]

### 帧1 (0s) - 开场/首帧
- [主体描述]
- [颜色/光线]
- [构图特点]
- [氛围/情绪]

### 帧2-3
- [画面变化描述]
- [主体动作/状态]
- [光影变化]

### 帧4-6
- [中期画面特征]
- [关键元素出现]
- [动作/变化描述]

### 帧7-9
- [后期画面特征]
- [结尾处理方式]
- [整体节奏变化]

## 视觉风格总结
- **主色调**: [具体颜色描述]
- **辅助色**: [具体颜色描述]
- **风格标签**: [3-5个具体标签]
- **光影效果**: [具体光线类型和效果]
- **构图**: [具体构图方式]
- **情绪**: [具体情绪关键词]

## 听觉特征分析（如适用）
- **声音/音乐类型**: [电子/古典/ASMR/氛围音乐等]
- **节奏特征**: [BPM估算或节奏描述]
- **情绪标签**: [治愈/放松/激励等]
- **与视觉的配合度**: [描述声音如何配合画面]

## 为什么数据好？（初步判断）
1. [基于数据表现的核心原因]
2. [视觉/听觉/文案维度的原因]
3. [赛道/时机维度的原因]
4. [其他可能原因]

---

## 🎯 AI 反推提示词（基于实际画面内容）

**重要：以下提示词必须基于实际关键帧画面的具体观察生成**

### 图像生成提示词（Midjourney/即梦）

**首帧/封面画面：**
```
[基于实际首帧画面的具体描述：主体类型、颜色、位置、光线、背景]
[风格关键词]
--ar 9:16 --v 6
```

**关键动作/变化画面：**
```
[基于实际动作帧的具体描述：手部动作、物体交互、光影变化]
[氛围关键词]
--ar 9:16 --v 6
```

**氛围/场景画面：**
```
[基于实际场景帧的具体描述：环境、光线、情绪]
[风格关键词]
--ar 9:16 --v 6
```

### 视频生成提示词（可灵/Runway/Pika）

```
Scene: [具体场景描述，基于实际画面观察]
Lighting: [具体光线描述，基于实际光影效果]
Camera: [运镜方式，基于实际视频节奏]
Action: [具体动作描述，基于实际关键帧变化]
Duration: [建议时长]
Style: [具体风格标签]
Mood: [具体情绪关键词]
```

### 声音/音乐生成提示词（Suno/Udio）

```
Style: [基于实际音频的具体音乐类型：电子/古典/ASMR/氛围音乐等]
Sounds: [具体声音元素描述]
Environment: [环境音特征]
Tempo: [基于实际音频的BPM或节奏特征]
[如果是ASMR：具体ASMR触发器类型，如tapping、scratching等]
Duration: [时长]
Mood: [基于实际音频的情绪标签]
```

### 拍摄/制作参数表

| 元素 | 具体参数（基于实际画面内容） |
|-----|---------------------------|
| 光源 | [具体光源类型、位置、数量] |
| 背景 | [具体背景描述] |
| 相机设置 | [基于画面质量的推测参数：ISO、光圈、快门] |
| 色调 | [具体主色、辅助色、色温] |
| 构图 | [具体构图方式：中心、三分法、对称等] |
| 动作 | [具体动作描述] |
| 音频 | [具体音频特征] |

---

## 分析任务要求

1. **基于实际观察**：所有分析必须基于实际关键帧图片的具体内容，不是通用描述
2. **具体可复刻**：所有反推提示词必须是具体的、可复刻的，不是通用模板
3. **结构化输出**：按照上述模块组织输出内容
4. **诚实标注**：如果无法确定某些细节，明确标注"需要进一步确认"
"""

    return prompt


def main():
    parser = argparse.ArgumentParser(description="生成 AI 分析提示词")
    parser.add_argument("metadata", help="metadata.json 文件路径")
    parser.add_argument("-o", "--output", help="输出提示词文件路径")
    
    args = parser.parse_args()
    
    # 读取元数据
    with open(args.metadata, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    # 检查是否有帧和音频
    metadata_dir = Path(args.metadata).parent
    has_frames = (metadata_dir / "frames").exists() and list((metadata_dir / "frames").glob("*.jpg"))
    has_audio = (metadata_dir / "audio.wav").exists()
    
    # 生成提示词
    prompt = generate_analysis_prompt(metadata, has_frames, has_audio)
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"提示词已保存至: {args.output}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
