"""
Backward compatibility - old tts_engine_lightweight.py

This file is kept for backward compatibility.
New code should use: from tts_engine import create_engine
"""

import warnings

# Re-export from new package location
from tts_engine.edge import EdgeTTSEngine
from tts_engine.piper import PiperTTSEngine
from tts_engine.kokoro import KokoroTTSEngine
from tts_engine import create_engine


# Keep old LightweightTTSEngine as alias to new factory
def LightweightTTSEngine(model_type: str = "piper"):
    """Deprecated: Use create_engine() instead."""
    warnings.warn(
        "LightweightTTSEngine is deprecated. Use: from tts_engine import create_engine",
        DeprecationWarning,
        stacklevel=2
    )
    return create_engine(model_type)


warnings.warn(
    "tts_engine_lightweight.py is deprecated. Use: from tts_engine import create_engine",
    DeprecationWarning,
    stacklevel=2
)

__all__ = [
    "LightweightTTSEngine",
    "EdgeTTSEngine",
    "PiperTTSEngine",
    "KokoroTTSEngine",
    "create_engine",
]
