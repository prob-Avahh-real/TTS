"""
TTS引擎单元测试 - Updated for new package structure
Tests tts_engine package core functionality
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# 导入conftest以设置mock
import tests.conftest  # noqa


class TestTTSEngine(unittest.TestCase):
    """TTSEngine类单元测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "test_output.wav")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_init_default(self, mock_cuda_available, mock_tts_class):
        """测试默认初始化"""
        mock_cuda_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_class.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        
        self.assertEqual(engine.device, "cpu")
        self.assertEqual(engine.model_name, "tts_models/multilingual/multi-dataset/xtts_v2")
        mock_tts_class.assert_called_once()
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_init_with_gpu(self, mock_cuda_available, mock_tts_class):
        """测试GPU初始化"""
        mock_cuda_available.return_value = True
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_class.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine(gpu=True)
        
        self.assertEqual(engine.device, "cuda")
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_init_custom_device(self, mock_cuda_available, mock_tts_class):
        """测试自定义设备"""
        mock_tts_instance = Mock()
        mock_tts_class.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine(device="cpu")
        
        self.assertEqual(engine.device, "cpu")
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_list_speakers(self, mock_torch, mock_tts):
        """测试列出说话者"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_instance.speakers = ["speaker1", "speaker2"]
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        speakers = engine.list_speakers()
        
        self.assertEqual(speakers, ["speaker1", "speaker2"])
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_list_speakers_empty(self, mock_torch, mock_tts):
        """测试空说话者列表"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_instance.speakers = None
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        speakers = engine.list_speakers()
        
        self.assertEqual(speakers, [])
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_synthesize_with_speaker_idx(self, mock_torch, mock_tts):
        """测试使用speaker_idx合成"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_instance.speakers = ["speaker1"]
        mock_tts_instance.tts_to_file = Mock()
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        engine.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
        result = engine.synthesize(
            text="测试文本",
            output_path=self.output_path,
            speaker_idx="speaker1",
            language="zh"
        )
        
        self.assertEqual(result, self.output_path)
        mock_tts_instance.tts_to_file.assert_called_once()
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_synthesize_with_speaker_wav(self, mock_torch, mock_tts):
        """测试使用speaker_wav合成"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_instance.tts_to_file = Mock()
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        engine.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
        reference_audio = os.path.join(self.temp_dir, "reference.wav")
        Path(reference_audio).touch()  # 创建临时文件
        
        result = engine.synthesize(
            text="测试文本",
            output_path=self.output_path,
            speaker_wav=reference_audio,
            language="zh"
        )
        
        self.assertEqual(result, self.output_path)
        mock_tts_instance.tts_to_file.assert_called_once()
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_synthesize_conflict(self, mock_torch, mock_tts):
        """测试同时指定speaker_wav和speaker_idx应该报错"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        
        with self.assertRaises(ValueError):
            engine.synthesize(
                text="测试文本",
                output_path=self.output_path,
                speaker_wav="ref.wav",
                speaker_idx="speaker1",
                language="zh"
            )
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_clone_voice(self, mock_torch, mock_tts):
        """测试语音克隆"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_instance.tts_to_file = Mock()
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        engine.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
        reference_audio = os.path.join(self.temp_dir, "reference.wav")
        Path(reference_audio).touch()
        
        result = engine.clone_voice(
            text="测试文本",
            reference_audio=reference_audio,
            output_path=self.output_path,
            language="zh"
        )
        
        self.assertEqual(result, self.output_path)
        mock_tts_instance.tts_to_file.assert_called_once()
    
    @patch('tts_engine.xtts.TTS')
    @patch('tts_engine.xtts.torch.cuda.is_available')
    def test_synthesize_batch(self, mock_torch, mock_tts):
        """测试批量合成"""
        mock_torch.cuda.is_available.return_value = False
        mock_tts_instance = Mock()
        mock_tts_instance.to.return_value = mock_tts_instance
        mock_tts_instance.speakers = ["speaker1"]
        mock_tts_instance.tts_to_file = Mock()
        mock_tts.return_value = mock_tts_instance
        
        from tts_engine.xtts import XTTSEngine as TTSEngine
        
        engine = TTSEngine()
        engine.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
        texts = ["文本1", "文本2", "文本3"]
        # 设置默认speaker避免 ValueError
        engine.speakers = ["speaker1"]
        output_paths = engine.synthesize_batch(
            texts=texts,
            output_dir=self.temp_dir,
            language="zh"
        )
        
        self.assertEqual(len(output_paths), 3)
        self.assertEqual(mock_tts_instance.tts_to_file.call_count, 3)


if __name__ == '__main__':
    unittest.main()
