"""
Backward compatibility - old tts_engine.py

This file is kept for backward compatibility.
New code should use: from tts_engine import create_engine
"""

import warnings

# Re-export from new package location
from tts_engine.xtts import XTTSEngine as TTSEngine

warnings.warn(
    "tts_engine.py is deprecated. Use: from tts_engine import create_engine",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ["TTSEngine"]
