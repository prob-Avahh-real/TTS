"""
Edge-TTS 真实集成测试
需要网络连接和 edge-tts 库
"""

import unittest
import os
import time
import tempfile
from pathlib import Path
import asyncio

# 检查依赖
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# 检查网络连接（简单检查）
try:
    import socket
    socket.create_connection(("www.microsoft.com", 443), timeout=3)
    NETWORK_AVAILABLE = True
except (OSError, socket.timeout):
    NETWORK_AVAILABLE = False


@unittest.skipUnless(EDGE_TTS_AVAILABLE, "Edge-TTS 未安装")
@unittest.skipUnless(NETWORK_AVAILABLE, "网络不可用")
class TestEdgeTTSIntegration(unittest.TestCase):
    """Edge-TTS 真实集成测试（需要网络）"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "outputs"
        self.output_dir.mkdir(exist_ok=True)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_list_chinese_voices(self):
        """测试列出中文语音"""
        async def _test():
            voices = await edge_tts.list_voices()
            chinese_voices = [v for v in voices if "zh-CN" in v["Locale"]]
            self.assertGreater(len(chinese_voices), 0, "应该找到至少一个中文语音")
            return chinese_voices
        
        chinese_voices = asyncio.run(_test())
        print(f"\n找到 {len(chinese_voices)} 个中文语音")
    
    def test_synthesize_single(self):
        """测试单个语音合成"""
        async def _test():
            voices = await edge_tts.list_voices()
            chinese_voices = [v for v in voices if "zh-CN" in v["Locale"]]
            self.assertGreater(len(chinese_voices), 0, "需要至少一个中文语音")
            
            test_voice = chinese_voices[0]["ShortName"]
            test_text = "这是Edge-TTS集成测试，验证真实网络调用和语音合成功能。"
            
            output_path = self.output_dir / "integration_test.wav"
            
            start_time = time.time()
            communicate = edge_tts.Communicate(test_text, test_voice)
            await communicate.save(str(output_path))
            elapsed_time = time.time() - start_time
            
            # 验证文件存在且有内容
            self.assertTrue(output_path.exists(), "输出文件应该存在")
            self.assertGreater(output_path.stat().st_size, 0, "输出文件应该有内容")
            
            print(f"\n✅ 合成成功:")
            print(f"   文件: {output_path}")
            print(f"   大小: {output_path.stat().st_size / 1024:.2f} KB")
            print(f"   耗时: {elapsed_time:.2f} 秒")
            print(f"   速度: {len(test_text)/elapsed_time:.1f} 字/秒")
            
            return output_path
        
        result = asyncio.run(_test())
        self.assertIsNotNone(result)
    
    def test_synthesize_multiple_voices(self):
        """测试多个语音合成"""
        async def _test():
            voices = await edge_tts.list_voices()
            chinese_voices = [v for v in voices if "zh-CN" in v["Locale"]]
            self.assertGreaterEqual(len(chinese_voices), 2, "需要至少2个中文语音")
            
            test_voices = [v["ShortName"] for v in chinese_voices[:2]]
            test_text = "测试多语音合成功能。"
            
            results = []
            for i, voice in enumerate(test_voices):
                output_path = self.output_dir / f"multi_voice_{i+1}.wav"
                
                communicate = edge_tts.Communicate(test_text, voice)
                await communicate.save(str(output_path))
                
                self.assertTrue(output_path.exists())
                results.append(output_path)
            
            self.assertEqual(len(results), 2, "应该生成2个文件")
            print(f"\n✅ 多语音测试成功，生成了 {len(results)} 个文件")
            
            return results
        
        results = asyncio.run(_test())
        self.assertEqual(len(results), 2)
    
    def test_edge_engine_integration(self):
        """测试 EdgeTTSEngine 集成"""
        from tts_engine.edge import EdgeTTSEngine
        
        engine = EdgeTTSEngine()
        
        # 列出语音
        voices = engine.list_voices("zh")
        self.assertGreater(len(voices), 0, "应该能找到中文语音")
        
        # 合成语音
        output_path = self.output_dir / "engine_test.wav"
        result = engine.synthesize(
            text="这是使用EdgeTTSEngine的集成测试。",
            output_path=str(output_path),
            language="zh"
        )
        
        self.assertTrue(Path(result).exists())
        self.assertGreater(Path(result).stat().st_size, 0)
        print(f"\n✅ EdgeTTSEngine 集成测试成功: {result}")
    
    def test_batch_synthesis(self):
        """测试批量合成"""
        from tts_engine.edge import EdgeTTSEngine
        
        engine = EdgeTTSEngine()
        
        texts = [
            "第一段：批量合成测试。",
            "第二段：验证多个文本的处理能力。",
            "第三段：确保所有文件都能正常生成。",
        ]
        
        output_paths = engine.synthesize_batch(
            texts=texts,
            output_dir=str(self.output_dir),
            language="zh"
        )
        
        self.assertEqual(len(output_paths), len(texts))
        for path in output_paths:
            self.assertTrue(Path(path).exists())
            self.assertGreater(Path(path).stat().st_size, 0)
        
        print(f"\n✅ 批量合成测试成功，生成了 {len(output_paths)} 个文件")


if __name__ == '__main__':
    unittest.main()
