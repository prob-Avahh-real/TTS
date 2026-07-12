"""
测试配置和fixtures
在导入被测试模块之前mock依赖
"""

import sys
from unittest.mock import MagicMock

# Mock torch before any imports
if 'torch' not in sys.modules:
    mock_torch = MagicMock()
    mock_torch.cuda.is_available.return_value = False
    sys.modules['torch'] = mock_torch

# Mock TTS before any imports
if 'TTS' not in sys.modules:
    sys.modules['TTS'] = MagicMock()
    sys.modules['TTS.api'] = MagicMock()

# Mock edge_tts before any imports
if 'edge_tts' not in sys.modules:
    sys.modules['edge_tts'] = MagicMock()
