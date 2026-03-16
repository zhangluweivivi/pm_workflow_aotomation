#!/usr/bin/env python3
"""
小红书笔记一键分析
整合下载、提取、分析全流程
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# 脚本路径
SCRIPTS_DIR = Path(__file__).parent
DOWNLOAD_SCRIPT = SCRIPTS_DIR / "download_and_extract.py"
PROMPT_SCRIPT = SCRIPTS_DIR / "generate_prompt.py"


def run_download(url: str, output_dir: str) -> tuple[dict, Path]:
    """运行下载脚本，返回元数据和实际输出目录"""
    cmd = [
        sys.executable, str(DOWNLOAD_SCRIPT),
        url,
        "-o", output_dir
    ]
    
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"下载失败: {result.stderr}")
        sys.exit(1)
    
    print(result.stdout)
    
    # 从输出中提取实际的子目录路径
    actual_output_dir = Path(output_dir)
    for line in result.stdout.split('\n'):
        if '输出目录:' in line:
            # 提取路径
            path_str = line.split('输出目录:')[-1].strip()
            actual_output_dir = Path(path_str)
            break
    
    # 解析输出获取元数据
    try:
        # 从输出中提取元数据
        lines = result.stdout.split('\n')
        for line in lines:
            if line.strip().startswith('{'):
                return json.loads(line), actual_output_dir
    except:
        pass
    
    # 从文件读取
    meta_path = actual_output_dir / "metadata.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f), actual_output_dir
    
    return {}, actual_output_dir


def generate_prompt(output_dir: str) -> str:
    """生成分析提示词"""
    meta_path = Path(output_dir) / "metadata.json"
    prompt_path = Path(output_dir) / "analysis_prompt.txt"
    
    cmd = [
        sys.executable, str(PROMPT_SCRIPT),
        str(meta_path),
        "-o", str(prompt_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"生成提示词失败: {result.stderr}")
        return ""
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="小红书笔记一键分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python analyze.py "https://www.xiaohongshu.com/explore/xxx"
  python analyze.py "https://www.xiaohongshu.com/explore/xxx" -o ./my_analysis
  python analyze.py "https://www.xiaohongshu.com/explore/xxx" --skip-download
        """
    )
    parser.add_argument("url", help="小红书笔记链接")
    parser.add_argument("-o", "--output", default="/Users/zlw/clawd/analysis", help="输出目录")
    parser.add_argument("--skip-download", action="store_true", help="跳过下载（使用已有数据）")
    parser.add_argument("--prompt-only", action="store_true", help="仅生成提示词")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎯 小红书笔记创意分析工具")
    print("=" * 60)
    
    base_output_dir = Path(args.output)
    
    # 步骤1: 下载
    if not args.skip_download and not args.prompt_only:
        print("\n📥 步骤 1/3: 下载笔记内容...")
        metadata, output_path = run_download(args.url, str(base_output_dir))
    else:
        print("\n⏭️  跳过下载，使用已有数据")
        # 尝试找到笔记ID子目录
        subdirs = [d for d in base_output_dir.iterdir() if d.is_dir()]
        if len(subdirs) == 1:
            output_path = subdirs[0]
        else:
            output_path = base_output_dir
        meta_path = output_path / "metadata.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        else:
            print(f"错误: 找不到元数据文件 {meta_path}")
            sys.exit(1)
    
    # 步骤2: 生成提示词
    print("\n📝 步骤 2/3: 生成 AI 分析提示词...")
    prompt = generate_prompt(str(output_path))
    
    if prompt:
        print(f"  ✓ 提示词已保存至: {output_path / 'analysis_prompt.txt'}")
    
    # 步骤3: 输出摘要
    print("\n📊 步骤 3/3: 分析摘要")
    print("-" * 60)
    print(f"笔记类型: {'视频' if metadata.get('has_video') else '图文'}")
    print(f"作者: {metadata.get('author', {}).get('nickname', '')}")
    print(f"点赞: {metadata.get('stats', {}).get('likes', '0')}")
    print(f"收藏: {metadata.get('stats', {}).get('collects', '0')}")
    print(f"标签: {', '.join(metadata.get('tags', [])[:5])}")
    
    # 检查下载的文件
    frames_dir = output_path / "frames"
    has_frames = frames_dir.exists() and list(frames_dir.glob("*.jpg"))
    has_audio = (output_path / "audio.wav").exists()
    has_images = list(output_path.glob("image_*.jpg"))
    
    print(f"\n已下载:")
    if has_frames:
        print(f"  📹 视频关键帧: {len(list(frames_dir.glob('*.jpg')))} 张")
    if has_audio:
        print(f"  🔊 音频: audio.wav")
    if has_images:
        print(f"  🖼️  图片: {len(has_images)} 张")
    
    print("\n" + "=" * 60)
    print(f"✅ 分析准备完成！")
    print(f"📁 输出目录: {output_path.absolute()}")
    print("=" * 60)
    
    # 输出下一步建议
    print("\n🚀 下一步:")
    print("  1. 查看关键帧: 打开 frames/ 目录查看视频截图")
    print("  2. AI 分析: 将 analysis_prompt.txt 和关键帧发送给 AI 进行分析")
    print("  3. 获取创意: 根据 AI 分析结果生成你的复刻版本")
    
    # 如果安装了 rich，显示更漂亮的输出
    try:
        from rich import print as rprint
        from rich.panel import Panel
        from rich.tree import Tree
        
        tree = Tree(f"📁 {output_path.name}")
        tree.add("📄 metadata.json")
        tree.add("📄 downloaded.json")
        tree.add("📝 analysis_prompt.txt")
        
        if has_frames:
            tree.add(f"📹 frames/ ({len(list(frames_dir.glob('*.jpg')))} frames)")
        if has_audio:
            tree.add("🔊 audio.wav")
        if has_images:
            tree.add(f"🖼️  images/ ({len(has_images)} images)")
        
        rprint(Panel(tree, title="输出文件结构", border_style="green"))
    except ImportError:
        pass


if __name__ == "__main__":
    main()
