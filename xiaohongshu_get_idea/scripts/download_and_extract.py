#!/usr/bin/env python3
"""
小红书笔记下载与分析工具
使用 Kimi K2.5 Vision 进行视觉分析和提示词生成
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# 添加 xiaohongshu-skills 到路径
XHS_SKILLS_PATH = "/Users/zlw/clawd/agents-skills-personal/xiaohongshu-skills-main/scripts"
sys.path.insert(0, XHS_SKILLS_PATH)

from xhs.cdp import Browser


def parse_xhs_url(url: str) -> tuple[str, str]:
    """从小红书 URL 提取 feed_id 和 xsec_token"""
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    
    if len(path_parts) < 2 or path_parts[0] != "explore":
        raise ValueError(f"无效的小红书 URL: {url}")
    
    feed_id = path_parts[1]
    query_params = parse_qs(parsed.query)
    xsec_token = query_params.get("xsec_token", [""])[0]
    
    if not xsec_token:
        raise ValueError(f"URL 中缺少 xsec_token: {url}")
    
    return feed_id, xsec_token


def get_note_detail(feed_id: str, xsec_token: str) -> dict:
    """获取笔记详情"""
    browser = Browser(host="127.0.0.1", port=18800)
    browser.connect()
    
    page = browser.new_page()
    url = f"https://www.xiaohongshu.com/explore/{feed_id}?xsec_token={xsec_token}&xsec_source=pc_feed"
    page.navigate(url)
    page.wait_for_load()
    time.sleep(2)
    
    js_code = f"""
    (() => {{
        const state = window.__INITIAL_STATE__;
        if (state && state.note && state.note.noteDetailMap) {{
            const detail = state.note.noteDetailMap["{feed_id}"];
            if (detail) return JSON.stringify(detail);
        }}
        return "";
    }})()
    """
    
    result = page.evaluate(js_code)
    browser.close()
    
    if not result:
        raise RuntimeError("无法获取笔记数据")
    
    return json.loads(result)


def download_media(note_data: dict, output_dir: str) -> dict:
    """下载媒体文件"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    note = note_data.get("note", {})
    note_type = note.get("type", "normal")
    
    downloaded = {
        "type": note_type,
        "images": [],
        "video": None,
        "audio": None,
        "frames": [],
        "duration": 0
    }
    
    if note_type == "video":
        video_info = note.get("video", {}) or note.get("videoList", [{}])[0]
        stream_data = video_info.get("media", {}).get("stream") or video_info.get("stream")
        
        if stream_data:
            streams = stream_data.get("h264", [{}])[0]
            video_url = streams.get("masterUrl", "")
            
            if video_url:
                video_path = output_path / "video.mp4"
                print(f"下载视频: {video_url[:60]}...")
                subprocess.run(
                    ["curl", "-L", "-o", str(video_path), video_url],
                    check=True, capture_output=True
                )
                downloaded["video"] = str(video_path)
                
                # 获取视频时长
                duration_result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
                    capture_output=True, text=True
                )
                if duration_result.returncode == 0:
                    downloaded["duration"] = float(duration_result.stdout.strip())
                
                # 提取关键帧
                frames_dir = output_path / "frames"
                frames_dir.mkdir(exist_ok=True)
                print("提取关键帧...")
                
                duration = downloaded["duration"]
                if duration > 0:
                    for i in range(10):
                        timestamp = duration * i / 9
                        if timestamp >= duration:
                            timestamp = duration - 0.1
                        frame_path = frames_dir / f"frame_{i+1:03d}.jpg"
                        subprocess.run([
                            "ffmpeg", "-ss", str(timestamp), "-i", str(video_path),
                            "-vframes", "1", "-q:v", "2",
                            "-vf", "scale=720:-1",
                            str(frame_path)
                        ], check=True, capture_output=True)
                        print(f"  帧 {i+1}/10 @ {timestamp:.1f}s")
                
                downloaded["frames"] = sorted([str(f) for f in frames_dir.glob("frame_*.jpg")])
                
                # 提取音频
                audio_path = output_path / "audio.wav"
                print("提取音频...")
                subprocess.run([
                    "ffmpeg", "-i", str(video_path),
                    "-vn", "-acodec", "pcm_s16le",
                    "-ar", "44100", "-ac", "2",
                    str(audio_path)
                ], check=True, capture_output=True)
                downloaded["audio"] = str(audio_path)
    else:
        # 下载图片
        image_list = note.get("imageList", [])
        for i, img in enumerate(image_list):
            img_url = img.get("urlDefault", "")
            if img_url:
                img_path = output_path / f"image_{i+1:03d}.jpg"
                print(f"下载图片 {i+1}: {img_url[:50]}...")
                subprocess.run(
                    ["curl", "-L", "-o", str(img_path), img_url],
                    check=True, capture_output=True
                )
                downloaded["images"].append(str(img_path))
    
    return downloaded


def analyze_with_kimi(frames: list[str], duration: float, api_key: str) -> dict:
    """使用 Kimi K2.5 分析关键帧"""
    import base64
    import requests
    
    if not frames or not api_key:
        return {}
    
    frame_count = len(frames)
    frame_descriptions = [f"帧{i+1} ({duration * i / max(frame_count - 1, 1):.1f}s)" for i in range(frame_count)]
    
    prompt = f"""你是一个专业的视觉内容分析师。请分析这个视频的 {frame_count} 张关键帧，生成结构化的视觉分析报告。

关键帧时间点: {', '.join(frame_descriptions)}

请输出以下格式的 JSON：
{{
  "overall_style": "整体视觉风格",
  "color_palette": {{"primary": "主色", "secondary": "辅助色", "accent": "点缀色"}},
  "style_tags": ["标签1", "标签2", "标签3"],
  "lighting": "光影效果",
  "composition": "构图特点",
  "mood": "情绪氛围",
  "visual_summary": "视觉总结"
}}

只输出纯 JSON，不要包含 ```json 标记"""
    
    try:
        content = [{"type": "text", "text": prompt}]
        
        for frame_path in frames[:3]:
            if os.path.exists(frame_path):
                with open(frame_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode("utf-8")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                })
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "moonshot-v1-32k-vision-preview",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.3,
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers=headers, json=payload, timeout=120
        )
        response.raise_for_status()
        
        text = response.json()["choices"][0]["message"]["content"]
        text = text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(text)
        
    except Exception as e:
        print(f"  ⚠️ Kimi 分析失败: {e}")
        return {}


def generate_prompts_with_kimi(metadata: dict, frames: list[str], api_key: str) -> dict:
    """使用 Kimi 生成提示词"""
    import base64
    import requests
    
    if not api_key:
        return {}
    
    title = metadata.get("title", "")
    desc = metadata.get("description", "")
    tags = metadata.get("tags", [])
    visual = metadata.get("visual_analysis", {})
    
    prompt_text = f"""你是 AI 提示词工程师。请根据以下信息生成可直接使用的 AI 提示词。

笔记: {title}
描述: {desc[:100]}
标签: {', '.join(tags[:5])}
风格: {visual.get('overall_style', 'N/A')}
色彩: {visual.get('color_palette', {}).get('primary', 'N/A')}
情绪: {visual.get('mood', 'N/A')}

请输出 JSON 格式：
{{
  "image_prompt": {{"midjourney": "...", "kling": "..."}},
  "video_prompt": {{"kling": "...", "runway": "..."}},
  "audio_prompt": {{"suno": "..."}},
  "copywriting": {{"title_options": ["..."], "description_template": "..."}}
}}

只输出纯 JSON"""
    
    try:
        content = [{"type": "text", "text": prompt_text}]
        
        for frame_path in frames[:2]:
            if os.path.exists(frame_path):
                with open(frame_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode("utf-8")
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                })
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "moonshot-v1-32k-vision-preview",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.4,
            "max_tokens": 1500
        }
        
        response = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers=headers, json=payload, timeout=120
        )
        response.raise_for_status()
        
        text = response.json()["choices"][0]["message"]["content"]
        text = text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(text)
        
    except Exception as e:
        print(f"  ⚠️ 提示词生成失败: {e}")
        return {}


def generate_analysis_report(metadata: dict, prompts: dict, output_dir: str) -> str:
    """生成分析报告"""
    title = metadata.get("title", "")
    desc = metadata.get("description", "")
    tags = metadata.get("tags", [])
    author = metadata.get("author", {}).get("nickname", "")
    stats = metadata.get("stats", {})
    duration = metadata.get("video_duration_formatted", "")
    visual = metadata.get("visual_analysis", {})
    
    img = prompts.get("image_prompt", {})
    vid = prompts.get("video_prompt", {})
    aud = prompts.get("audio_prompt", {})
    copy = prompts.get("copywriting", {})
    
    content = f"""# 小红书笔记分析报告

## 📊 笔记基础信息
- **标题**: {title}
- **作者**: {author}
- **类型**: {'视频' if metadata.get('has_video') else '图文'}
- **点赞**: {stats.get('likes', '0')}
- **收藏**: {stats.get('collects', '0')}
- **评论**: {stats.get('comments', '0')}
- **标签**: {', '.join(tags[:8])}
- **描述**: {desc[:150] if desc else '(无)'}{'...' if desc and len(desc) > 150 else ''}
- **视频时长**: {duration if duration else 'N/A'}

---

## 🎨 视觉分析（AI 生成）

### 整体风格
{visual.get('overall_style', '待分析')}

### 色彩方案
- **主色调**: {visual.get('color_palette', {}).get('primary', '待分析')}
- **辅助色**: {visual.get('color_palette', {}).get('secondary', '待分析')}
- **点缀色**: {visual.get('color_palette', {}).get('accent', '待分析')}

### 风格标签
{', '.join(visual.get('style_tags', ['待分析']))}

### 光影与构图
- **光影**: {visual.get('lighting', '待分析')}
- **构图**: {visual.get('composition', '待分析')}
- **情绪**: {visual.get('mood', '待分析')}

### 视觉总结
{visual.get('visual_summary', '待分析')}

---

## 🎯 AI 反推提示词（可直接使用）

### 🖼️ 生图提示词

#### Midjourney
```
{img.get('midjourney', '（待生成）')}
```

#### 可灵 AI
```
{img.get('kling', '（待生成）')}
```

---

### 🎬 生视频提示词

#### 可灵 AI
```
{vid.get('kling', '（待生成）')}
```

#### Runway
```
{vid.get('runway', '（待生成）')}
```

---

### 🎵 生音频提示词

#### Suno AI
```
{aud.get('suno', '（待生成）')}
```

---

### ✍️ 文案仿写

#### 标题选项
"""
    
    for i, opt in enumerate(copy.get('title_options', ['（待生成）']), 1):
        content += f"{i}. {opt}\n"
    
    content += f"""
#### 描述模板
```
{copy.get('description_template', '（待生成）')}
```

---

## 📁 文件清单
- `video.mp4` - 原始视频
- `audio.wav` - 提取的音频
- `frames/` - 关键帧图片
- `metadata.json` - 完整元数据

---

*生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return content


def main():
    parser = argparse.ArgumentParser(description="小红书笔记下载与分析")
    parser.add_argument("url", help="小红书笔记链接")
    parser.add_argument("-o", "--output", default="/Users/zlw/clawd/analysis", help="输出目录")
    parser.add_argument("--skip-download", action="store_true", help="跳过媒体下载")
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = os.environ.get("KIMI_API_KEY", "")
    if not api_key:
        print("⚠️ 警告: 未设置 KIMI_API_KEY 环境变量，将使用基础模板")
    
    print("=" * 50)
    print("小红书笔记分析工具 (Kimi Vision)")
    print("=" * 50)
    
    # 解析 URL
    print("\n[1/4] 解析链接...")
    try:
        feed_id, xsec_token = parse_xhs_url(args.url)
        print(f"  Feed ID: {feed_id}")
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    output_dir = Path(args.output) / feed_id
    print(f"  输出目录: {output_dir}")
    
    # 获取笔记详情
    print("\n[2/4] 获取笔记详情...")
    try:
        note_data = get_note_detail(feed_id, xsec_token)
        print("  ✓ 数据获取成功")
    except Exception as e:
        print(f"  ✗ 获取失败: {e}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 下载媒体
    video_duration = 0
    downloaded = {"frames": [], "video": None, "audio": None}
    
    if not args.skip_download:
        print("\n[3/4] 下载媒体内容...")
        try:
            downloaded = download_media(note_data, str(output_dir))
            if downloaded["video"]:
                print(f"  ✓ 视频 + 关键帧({len(downloaded['frames'])}) + 音频")
                video_duration = downloaded.get("duration", 0)
            else:
                print(f"  ✓ 图片: {len(downloaded['images'])} 张")
            
            with open(output_dir / "downloaded.json", "w", encoding="utf-8") as f:
                json.dump(downloaded, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  ⚠️ 下载失败: {e}")
    
    # AI 视觉分析
    visual_analysis = {}
    if api_key and downloaded.get("frames"):
        print("\n[4/5] AI 视觉分析 (Kimi)...")
        visual_analysis = analyze_with_kimi(downloaded["frames"], video_duration, api_key)
        if visual_analysis:
            print(f"  ✓ 风格: {visual_analysis.get('overall_style', 'N/A')[:40]}...")
    
    # 提取元数据
    print("\n[5/5] 提取元数据...")
    note = note_data.get("note", {})
    interact = note.get("interactInfo", {})
    user = note.get("user", {})
    desc = note.get("desc", "")
    
    metadata = {
        "note_id": note.get("noteId", ""),
        "title": note.get("title", ""),
        "description": re.sub(r'#\S+', '', desc).strip(),
        "tags": re.findall(r'#([^#\s]+)', desc),
        "type": note.get("type", "normal"),
        "author": {"nickname": user.get("nickname", ""), "user_id": user.get("userId", "")},
        "stats": {
            "likes": interact.get("likedCount", "0"),
            "collects": interact.get("collectedCount", "0"),
            "comments": interact.get("commentCount", "0")
        },
        "has_video": note.get("type") == "video",
        "video_duration": video_duration,
        "video_duration_formatted": f"{int(video_duration // 60)}分{int(video_duration % 60)}秒" if video_duration > 0 else "",
        "visual_analysis": visual_analysis
    }
    
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 元数据已保存")
    
    # 生成提示词
    prompts = {}
    if api_key and downloaded.get("frames"):
        print("\n[6/6] 生成 AI 提示词 (Kimi)...")
        prompts = generate_prompts_with_kimi(metadata, downloaded["frames"], api_key)
        if prompts:
            print("  ✓ 生图/视频/音频提示词已生成")
    
    # 生成分析报告
    print("\n[7/6] 生成分析报告...")
    report = generate_analysis_report(metadata, prompts, str(output_dir))
    with open(output_dir / "analysis_prompt.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  ✓ 报告已保存")
    
    print("\n" + "=" * 50)
    print(f"✅ 完成！输出目录: {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
