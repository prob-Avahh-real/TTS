"""
轻量级TTS引擎单元测试 - Updated for new package structure
测试 tts_engine 包的轻量级引擎功能
"""

import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock

# 导入conftest以设置基础 mock（sys.modules 注入）
import tests.conftest  # noqa


class TestLightweightTTSEngine(unittest.TestCase):
    """LightweightTTSEngine 类单元测试"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "test_output.wav")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_edge_engine_init(self):
        """测试 Edge-TTS 引擎初始化"""
        edge_mock = MagicMock()
        edge_mock.list_voices = AsyncMock(return_value=[])
        edge_mock.Communicate = MagicMock()

        with patch.dict("sys.modules", {"edge_tts": edge_mock}):
            from tts_engine.edge import EdgeTTSEngine
            engine = EdgeTTSEngine()
            self.assertEqual(engine.model_type, "edge")
            self.assertEqual(engine.engine_type, "edge")

    def test_edge_engine_init_fail(self):
        """测试 Edge-TTS 引擎初始化失败"""
        with patch.dict("sys.modules", {"edge_tts": None}):
            from tts_engine.edge import EdgeTTSEngine
            with self.assertRaises(ImportError):
                EdgeTTSEngine()

    def test_edge_list_voices(self):
        """测试 Edge-TTS 列出语音"""
        mock_voices = [
            {"ShortName": "zh-CN-XiaoxiaoNeural", "Locale": "zh-CN"},
            {"ShortName": "en-US-AriaNeural", "Locale": "en-US"},
        ]

        edge_mock = MagicMock()
        edge_mock.list_voices = AsyncMock(return_value=mock_voices)
        edge_mock.Communicate = MagicMock()

        with patch.dict("sys.modules", {"edge_tts": edge_mock}):
            from tts_engine.edge import EdgeTTSEngine
            engine = EdgeTTSEngine()
            voices = engine.list_voices("zh")
            self.assertGreater(len(voices), 0)

    def test_edge_synthesize(self):
        """测试 Edge-TTS 合成（模拟写文件）"""

        async def fake_save(path):
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                f.write(b"RIFF\x00\x00\x00\x00WAVE")

        class FakeComm:
            def __init__(self, text, voice):
                self.text = text
                self.voice = voice

            async def save(self, path):
                return await fake_save(path)

        edge_mock = MagicMock()
        edge_mock.list_voices = AsyncMock(
            return_value=[{"ShortName": "zh-CN-XiaoxiaoNeural", "Locale": "zh-CN"}]
        )
        edge_mock.Communicate = FakeComm

        with patch.dict("sys.modules", {"edge_tts": edge_mock}):
            from tts_engine.edge import EdgeTTSEngine
            engine = EdgeTTSEngine()
            result = engine._synthesize_edge(
                "测试文本", self.output_path, "zh-CN-XiaoxiaoNeural", "zh"
            )
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 0)

    def test_piper_engine_init(self):
        """测试 Piper TTS 引擎初始化"""
        mock_voice_cls = MagicMock()
        piper_mock = MagicMock()
        piper_mock.PiperVoice = mock_voice_cls

        with patch.dict("sys.modules", {"piper": piper_mock}):
            from tts_engine.piper import PiperTTSEngine
            engine = PiperTTSEngine()
            self.assertEqual(engine.model_type, "piper")
            self.assertEqual(engine.engine_type, "piper")

    def test_piper_synthesize(self):
        """测试 Piper TTS 合成（模拟写文件）"""
        mock_voice = Mock()
        mock_voice.synthesize = Mock()
        piper_mock = MagicMock()
        piper_mock.PiperVoice.load.return_value = mock_voice

        with patch.dict("sys.modules", {"piper": piper_mock}):
            from tts_engine.piper import PiperTTSEngine
            engine = PiperTTSEngine()

            # 创建临时模型文件（路径传入但被 mock）
            model_path = os.path.join(self.temp_dir, "test.onnx")
            config_path = os.path.join(self.temp_dir, "test.onnx.json")
            Path(model_path).touch()
            Path(config_path).touch()

            result = engine._synthesize_piper(
                "测试文本", self.output_path, "test", "zh"
            )

            self.assertEqual(result, self.output_path)
            mock_voice.synthesize.assert_called_once()

    def test_synthesize_batch(self):
        """测试批量合成"""
        from tts_engine import BaseTTSEngine

        with patch.object(BaseTTSEngine, "synthesize") as mock_synth:
            mock_synth.return_value = self.output_path

            engine = BaseTTSEngine(name="test")
            texts = ["文本1", "文本2", "文本3"]

            output_paths = engine.synthesize_batch(
                texts=texts, output_dir=self.temp_dir
            )

            self.assertEqual(len(output_paths), 3)
            self.assertEqual(mock_synth.call_count, 3)


if __name__ == "__main__":
    unittest.main()
