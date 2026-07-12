"""
测试轻量级TTS模型
演示如何使用不同的轻量级TTS引擎
"""

import os
import time
import sys
from pathlib import Path

# 创建输出目录
os.makedirs("outputs", exist_ok=True)


def test_edge_tts():
    """测试 Edge-TTS（Microsoft云端服务）"""
    print("\n" + "=" * 60)
    print("测试 1: Edge-TTS（Microsoft云端服务）")
    print("=" * 60)
    
    try:
        import edge_tts
        import asyncio
        
        print("✅ Edge-TTS 已安装")
        
        async def test_synthesis():
            # 列出可用语音
            print("\n正在获取可用中文语音...")
            voices = await edge_tts.list_voices()
            chinese_voices = [v for v in voices if "zh-CN" in v["Locale"]]
            
            print(f"找到 {len(chinese_voices)} 个中文语音")
            print("\n前5个中文语音:")
            for i, voice in enumerate(chinese_voices[:5]):
                print(f"  {i+1}. {voice['ShortName']} - {voice['Gender']} - {voice['Locale']}")
            
            # 选择一个语音进行测试
            test_voice = chinese_voices[0]["ShortName"]
            print(f"\n使用语音: {test_voice}")
            
            # 测试文本
            test_text = "你好，这是使用Edge-TTS生成的语音测试。Edge-TTS是Microsoft提供的云端文本转语音服务，无需本地模型，质量很高。"
            
            # 合成语音
            print(f"\n正在合成语音...")
            start_time = time.time()
            
            output_path = "outputs/test_edge_tts.wav"
            communicate = edge_tts.Communicate(test_text, test_voice)
            await communicate.save(output_path)
            
            elapsed_time = time.time() - start_time
            
            # 检查文件大小
            file_size = os.path.getsize(output_path) / 1024  # KB
            
            print(f"✅ 合成完成！")
            print(f"   - 输出文件: {output_path}")
            print(f"   - 文件大小: {file_size:.2f} KB")
            print(f"   - 耗时: {elapsed_time:.2f} 秒")
            print(f"   - 文本长度: {len(test_text)} 字")
            print(f"   - 速度: {len(test_text)/elapsed_time:.1f} 字/秒")
            
            return True
        
        result = asyncio.run(test_synthesis())
        return result
        
    except ImportError:
        print("❌ Edge-TTS 未安装")
        print("\n安装命令:")
        print("  pip install edge-tts")
        print("\n如果遇到SSL证书问题，可以尝试:")
        print("  pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org edge-tts")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_piper_tts():
    """测试 Piper TTS（超轻量级）"""
    print("\n" + "=" * 60)
    print("测试 2: Piper TTS（超轻量级，25-60MB）")
    print("=" * 60)
    
    try:
        # 尝试导入piper
        try:
            from piper import PiperVoice
            print("✅ Piper TTS Python包已安装")
        except ImportError:
            print("⚠️  Piper TTS Python包未安装")
            print("\nPiper TTS 安装说明:")
            print("  1. 安装Python包:")
            print("     pip install piper-tts")
            print("\n  2. 下载语音模型（从以下地址）:")
            print("     https://github.com/rhasspy/piper/releases")
            print("     或使用命令行:")
            print("     piper download --language zh_CN")
            print("\n  3. 中文语音模型示例:")
            print("     - zh_CN-xiaoyan-medium.onnx")
            print("     - zh_CN-xiaoyan-medium.onnx.json")
            return False
        
        # 检查是否有可用的语音模型
        print("\n正在查找Piper语音模型...")
        
        # 常见的模型路径
        possible_paths = [
            "~/.local/share/piper/voices",
            "./voices",
            "./piper_voices"
        ]
        
        found_models = []
        for base_path in possible_paths:
            expanded_path = os.path.expanduser(base_path)
            if os.path.exists(expanded_path):
                for file in os.listdir(expanded_path):
                    if file.endswith(".onnx") and not file.endswith(".onnx.json"):
                        model_name = file.replace(".onnx", "")
                        found_models.append({
                            "name": model_name,
                            "onnx": os.path.join(expanded_path, file),
                            "json": os.path.join(expanded_path, f"{model_name}.onnx.json")
                        })
        
        if not found_models:
            print("⚠️  未找到Piper语音模型文件")
            print("\n请下载语音模型:")
            print("  访问: https://github.com/rhasspy/piper/releases")
            print("  下载中文语音模型（.onnx 和 .onnx.json 文件）")
            return False
        
        print(f"✅ 找到 {len(found_models)} 个语音模型:")
        for model in found_models:
            print(f"   - {model['name']}")
        
        # 选择第一个中文模型
        chinese_model = None
        for model in found_models:
            if "zh" in model["name"].lower() or "cn" in model["name"].lower():
                chinese_model = model
                break
        
        if not chinese_model:
            chinese_model = found_models[0]
        
        print(f"\n使用模型: {chinese_model['name']}")
        
        # 加载模型
        print("正在加载模型...")
        voice = PiperVoice.load(chinese_model["onnx"], config_path=chinese_model["json"])
        
        # 测试文本
        test_text = "你好，这是使用Piper TTS生成的语音测试。Piper TTS是一个超轻量级的文本转语音引擎，模型只有25到60MB，可以在CPU上实时合成。"
        
        # 合成语音
        print(f"\n正在合成语音...")
        start_time = time.time()
        
        output_path = "outputs/test_piper_tts.wav"
        with open(output_path, "wb") as f:
            voice.synthesize(test_text, f)
        
        elapsed_time = time.time() - start_time
        
        # 检查文件大小
        file_size = os.path.getsize(output_path) / 1024  # KB
        
        print(f"✅ 合成完成！")
        print(f"   - 输出文件: {output_path}")
        print(f"   - 文件大小: {file_size:.2f} KB")
        print(f"   - 耗时: {elapsed_time:.2f} 秒")
        print(f"   - 文本长度: {len(test_text)} 字")
        print(f"   - 速度: {len(test_text)/elapsed_time:.1f} 字/秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_lightweight_engine():
    """测试轻量级引擎封装"""
    print("\n" + "=" * 60)
    print("测试 3: 轻量级引擎封装类")
    print("=" * 60)
    
    try:
        from tts_engine_lightweight import EdgeTTSEngine, PiperTTSEngine
        
        # 测试 Edge-TTS 引擎
        print("\n--- 测试 EdgeTTSEngine ---")
        try:
            edge_engine = EdgeTTSEngine()
            voices = edge_engine.list_voices("zh")
            print(f"可用中文语音数量: {len(voices)}")
            
            edge_engine.synthesize(
                text="这是使用EdgeTTSEngine封装的测试。",
                output_path="outputs/test_edge_engine.wav",
                language="zh"
            )
            print("✅ EdgeTTSEngine 测试成功")
        except Exception as e:
            print(f"⚠️  EdgeTTSEngine 测试失败: {e}")
        
        # 测试 Piper TTS 引擎
        print("\n--- 测试 PiperTTSEngine ---")
        try:
            piper_engine = PiperTTSEngine()
            piper_engine.synthesize(
                text="这是使用PiperTTSEngine封装的测试。",
                output_path="outputs/test_piper_engine.wav",
                language="zh"
            )
            print("✅ PiperTTSEngine 测试成功")
        except Exception as e:
            print(f"⚠️  PiperTTSEngine 测试失败: {e}")
            print("   提示: 需要先安装piper-tts并下载语音模型")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保 tts_engine_lightweight.py 文件存在")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def performance_comparison():
    """性能对比测试"""
    print("\n" + "=" * 60)
    print("性能对比测试")
    print("=" * 60)
    
    test_text = "这是一个性能测试文本，用于对比不同TTS引擎的速度和资源占用。"
    results = []
    
    # 测试 Edge-TTS
    try:
        import edge_tts
        import asyncio
        
        async def test_edge():
            start_time = time.time()
            communicate = edge_tts.Communicate(test_text, "zh-CN-XiaoxiaoNeural")
            await communicate.save("outputs/perf_edge.wav")
            return time.time() - start_time
        
        edge_time = asyncio.run(test_edge())
        edge_size = os.path.getsize("outputs/perf_edge.wav") / 1024
        
        results.append({
            "name": "Edge-TTS",
            "time": edge_time,
            "size": edge_size,
            "model_size": "0 MB"
        })
        print(f"✅ Edge-TTS: {edge_time:.2f}秒, 输出{edge_size:.2f}KB")
    except:
        print("⚠️  Edge-TTS 不可用")
    
    # 测试 Piper TTS（如果可用）
    try:
        from piper import PiperVoice
        
        # 这里需要实际的模型路径，暂时跳过
        print("⚠️  Piper TTS 需要模型文件，跳过性能测试")
    except:
        print("⚠️  Piper TTS 不可用")
    
    # 显示对比结果
    if results:
        print("\n性能对比结果:")
        print("-" * 60)
        print(f"{'模型':<15} {'耗时(秒)':<12} {'输出大小(KB)':<15} {'模型大小':<15}")
        print("-" * 60)
        for r in results:
            print(f"{r['name']:<15} {r['time']:<12.2f} {r['size']:<15.2f} {r['model_size']:<15}")
        print("-" * 60)


def main():
    """主测试函数"""
    print("=" * 60)
    print("轻量级TTS模型测试")
    print("=" * 60)
    print("\n本测试将验证以下轻量级TTS引擎:")
    print("  1. Edge-TTS (Microsoft云端服务)")
    print("  2. Piper TTS (超轻量级，25-60MB)")
    print("  3. 轻量级引擎封装类")
    
    results = []
    
    # 测试 Edge-TTS
    results.append(("Edge-TTS", test_edge_tts()))
    
    # 测试 Piper TTS
    results.append(("Piper TTS", test_piper_tts()))
    
    # 测试引擎封装
    results.append(("引擎封装", test_lightweight_engine()))
    
    # 性能对比
    performance_comparison()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败/跳过"
        print(f"{name:<20} {status}")
    
    print("\n生成的测试文件位于 outputs/ 目录:")
    if os.path.exists("outputs"):
        for file in os.listdir("outputs"):
            if file.endswith(".wav"):
                size = os.path.getsize(os.path.join("outputs", file)) / 1024
                print(f"  - {file} ({size:.2f} KB)")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
