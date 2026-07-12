"""
Edge-TTS 演示脚本
展示如何使用 Edge-TTS 进行语音合成
"""

import asyncio
import os
import time
from pathlib import Path


async def demo_edge_tts():
    """Edge-TTS 完整演示"""
    try:
        import edge_tts
    except ImportError:
        print("❌ Edge-TTS 未安装")
        print("\n请先安装:")
        print("  pip install edge-tts")
        print("\n如果遇到SSL问题:")
        print("  pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org edge-tts")
        return
    
    print("=" * 60)
    print("Edge-TTS 演示")
    print("=" * 60)
    
    # 1. 列出可用语音
    print("\n1. 获取可用语音列表...")
    voices = await edge_tts.list_voices()
    
    # 筛选中文语音
    chinese_voices = [v for v in voices if "zh-CN" in v["Locale"]]
    print(f"   找到 {len(chinese_voices)} 个中文语音")
    
    # 显示前10个中文语音
    print("\n   前10个中文语音:")
    for i, voice in enumerate(chinese_voices[:10], 1):
        gender_icon = "👨" if voice["Gender"] == "Male" else "👩"
        print(f"   {i:2d}. {voice['ShortName']:<30} {gender_icon} {voice['Locale']}")
    
    # 2. 选择语音进行测试
    print("\n2. 选择测试语音...")
    test_voices = [
        "zh-CN-XiaoxiaoNeural",  # 晓晓（女声）
        "zh-CN-YunxiNeural",     # 云希（男声）
        "zh-CN-YunyangNeural",   # 云扬（男声）
    ]
    
    # 创建输出目录
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # 3. 测试不同语音
    print("\n3. 测试不同语音合成...")
    test_texts = [
        "你好，我是晓晓，这是Edge-TTS的语音合成测试。",
        "你好，我是云希，Edge-TTS是Microsoft提供的云端文本转语音服务。",
        "你好，我是云扬，这个服务无需本地模型，质量很高。",
    ]
    
    results = []
    
    for i, (voice_name, text) in enumerate(zip(test_voices, test_texts)):
        if voice_name not in [v["ShortName"] for v in chinese_voices]:
            print(f"   ⚠️  语音 {voice_name} 不可用，跳过")
            continue
        
        output_path = output_dir / f"edge_tts_demo_{i+1}.wav"
        
        print(f"\n   测试 {i+1}: {voice_name}")
        print(f"   文本: {text}")
        
        start_time = time.time()
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(str(output_path))
        elapsed_time = time.time() - start_time
        
        file_size = output_path.stat().st_size / 1024
        
        results.append({
            "voice": voice_name,
            "time": elapsed_time,
            "size": file_size,
            "text_length": len(text)
        })
        
        print(f"   ✅ 完成: {output_path}")
        print(f"   ⏱️  耗时: {elapsed_time:.2f}秒")
        print(f"   📦 大小: {file_size:.2f}KB")
        print(f"   ⚡ 速度: {len(text)/elapsed_time:.1f}字/秒")
    
    # 4. 批量合成示例
    print("\n4. 批量合成示例...")
    batch_texts = [
        "第一段文本：今天天气真好。",
        "第二段文本：适合出去散步。",
        "第三段文本：享受美好的时光。",
    ]
    
    batch_outputs = []
    start_time = time.time()
    
    for i, text in enumerate(batch_texts):
        output_path = output_dir / f"edge_tts_batch_{i+1}.wav"
        communicate = edge_tts.Communicate(text, test_voices[0])
        await communicate.save(str(output_path))
        batch_outputs.append(output_path)
    
    batch_time = time.time() - start_time
    
    print(f"   ✅ 批量合成完成: {len(batch_texts)} 个文件")
    print(f"   ⏱️  总耗时: {batch_time:.2f}秒")
    print(f"   ⚡ 平均速度: {sum(len(t) for t in batch_texts)/batch_time:.1f}字/秒")
    
    # 5. 性能总结
    print("\n" + "=" * 60)
    print("性能总结")
    print("=" * 60)
    
    if results:
        print(f"\n{'语音':<30} {'耗时(秒)':<12} {'文件大小(KB)':<15} {'速度(字/秒)':<15}")
        print("-" * 60)
        for r in results:
            speed = r["text_length"] / r["time"]
            print(f"{r['voice']:<30} {r['time']:<12.2f} {r['size']:<15.2f} {speed:<15.1f}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print(f"\n所有输出文件保存在: {output_dir.absolute()}")
    print("\n生成的音频文件:")
    for file in sorted(output_dir.glob("edge_tts_*.wav")):
        size = file.stat().st_size / 1024
        print(f"  - {file.name} ({size:.2f} KB)")


if __name__ == "__main__":
    asyncio.run(demo_edge_tts())
