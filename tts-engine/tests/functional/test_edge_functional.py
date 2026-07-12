"""
Edge-TTS 功能级测试（使用假通信对象，无需真实网络）
"""

import os
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio


class FakeCommunicate:
    """模拟 edge_tts.Communicate.save 行为，写入一个空文件"""

    def __init__(self, text, voice):
        self.text = text
        self.voice = voice

    async def save(self, file_path: str):
        # 创建一个最小的 wav 文件占位
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(b"RIFF\x00\x00\x00\x00WAVE")  # 简单占位头
        return file_path


class TestEdgeFunctional(TestCase):
    """Edge-TTS 功能级测试（无网络，验证管线和文件输出）"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.output = os.path.join(self.tmpdir, "edge_func.wav")

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_edge_synthesize_pipeline(self):
        """验证 EdgeTTSEngine 管线：能调用到 Communicate.save 并生成文件"""
        # mock list_voices 返回中文语音
        async def fake_list_voices():
            return [{"ShortName": "zh-CN-XiaoxiaoNeural", "Locale": "zh-CN"}]

        edge_mock = MagicMock()
        edge_mock.list_voices = fake_list_voices
        edge_mock.Communicate = FakeCommunicate

        with patch.dict("sys.modules", {"edge_tts": edge_mock}):
            from tts_engine_lightweight import EdgeTTSEngine

            engine = EdgeTTSEngine()
            result = engine.synthesize(
                text="功能测试：Edge-TTS",
                output_path=self.output,
                language="zh",
            )

            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 0)
