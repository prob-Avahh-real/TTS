"""
XTTS 功能级测试（使用 mock，验证管线和参数处理）
"""

import os
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock


class FakeTTS:
    """模拟 TTS.api.TTS 的最简实现"""

    def __init__(self, model_name=None):
        self.model_name = model_name
        self.speakers = ["speaker1", "speaker2"]
        self.tts_to_file = MagicMock(side_effect=self._write_file)

    def to(self, device):
        return self

    def _write_file(self, *args, **kwargs):
        file_path = kwargs.get("file_path")
        if file_path:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(b"RIFF\x00\x00\x00\x00WAVE")
        return file_path


class TestXTTSFunctional(TestCase):
    """XTTS 功能级测试（无真实模型，验证调用链）"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.output = os.path.join(self.tmpdir, "xtts_func.wav")

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @patch("tts_engine.TTS", side_effect=lambda model_name=None: FakeTTS(model_name))
    @patch("tts_engine.torch")
    def test_xtts_synthesize_pipeline(self, mock_torch, mock_tts):
        """验证 XTTS 管线：能写出文件、默认 speaker 处理"""
        mock_torch.cuda.is_available.return_value = False

        from tts_engine import TTSEngine

        engine = TTSEngine()
        result = engine.synthesize(
            text="功能测试：XTTS",
            output_path=self.output,
            language="zh",
        )

        self.assertTrue(os.path.exists(result))
        self.assertGreater(os.path.getsize(result), 0)
        # 确认调用过 tts_to_file（检查实例本身）
        self.assertTrue(engine.tts.tts_to_file.called)
