"""
XTTS-v2 真实集成测试
需要 torch 和 TTS 库（模型较大，约1.8GB）
"""

import unittest
import os
import tempfile
from pathlib import Path

# 检查依赖
try:
    import torch
    import TTS
    XTTS_AVAILABLE = True
except ImportError:
    XTTS_AVAILABLE = False


@unittest.skipUnless(XTTS_AVAILABLE, "XTTS 依赖未安装（需要 torch 和 TTS）")
class TestXTTSIntegration(unittest.TestCase):
    """XTTS-v2 真实集成测试（需要下载大模型）"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "outputs"
        self.output_dir.mkdir(exist_ok=True)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @unittest.skip("需要下载1.8GB模型，跳过默认运行")
    def test_xtts_synthesis(self):
        """测试 XTTS-v2 语音合成（需要大模型）"""
        from tts_engine import TTSEngine
        
        engine = TTSEngine()
        
        # 列出说话者
        speakers = engine.list_speakers()
        print(f"\n可用说话者: {speakers}")
        
        # 合成语音
        output_path = self.output_dir / "xtts_integration.wav"
        result = engine.synthesize(
            text="这是XTTS-v2集成测试，验证真实模型调用。",
            output_path=str(output_path),
            language="zh"
        )
        
        self.assertTrue(Path(result).exists())
        self.assertGreater(Path(result).stat().st_size, 0)
        print(f"\n✅ XTTS-v2 集成测试成功: {result}")
    
    @unittest.skip("需要下载1.8GB模型，跳过默认运行")
    def test_voice_cloning(self):
        """测试语音克隆（需要参考音频）"""
        from tts_engine import TTSEngine
        
        engine = TTSEngine()
        
        # 需要提供参考音频文件
        reference_audio = "reference.wav"  # 需要用户提供
        
        if not Path(reference_audio).exists():
            self.skipTest("需要参考音频文件")
        
        output_path = self.output_dir / "cloned.wav"
        result = engine.clone_voice(
            text="这是语音克隆测试。",
            reference_audio=reference_audio,
            output_path=str(output_path),
            language="zh"
        )
        
        self.assertTrue(Path(result).exists())
        print(f"\n✅ 语音克隆测试成功: {result}")


if __name__ == '__main__':
    unittest.main()
