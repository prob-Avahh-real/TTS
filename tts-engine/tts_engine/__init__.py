"""
TTS Engine Package - Unified Text-to-Speech Interface

This package provides a clean abstraction over multiple TTS backends:
- XTTS (heavy, local model)
- Edge-TTS (lightweight, cloud-based)
- Piper TTS (lightweight, local)
- Kokoro TTS (lightweight, local)

Usage:
    from tts_engine import create_engine
    
    # Create engine by type
    engine = create_engine("edge")  # or "xtts", "piper", "kokoro"
    
    # Use unified interface
    engine.synthesize("Hello world", "output.wav")
"""

from typing import Protocol, Optional, List, Union, runtime_checkable
from pathlib import Path


@runtime_checkable
class TTSEngine(Protocol):
    """TTS Engine Protocol - all engines implement this interface"""
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        **kwargs
    ) -> str:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            **kwargs: Engine-specific options (voice, speaker, etc.)
            
        Returns:
            Path to generated audio file
        """
        ...
    
    def synthesize_batch(
        self,
        texts: List[str],
        output_dir: str,
        **kwargs
    ) -> List[str]:
        """
        Batch synthesize multiple texts.
        
        Args:
            texts: List of texts to synthesize
            output_dir: Output directory for audio files
            **kwargs: Engine-specific options
            
        Returns:
            List of paths to generated audio files
        """
        ...


class BaseTTSEngine:
    """
    Abstract base class for TTS engines.
    Implements common functionality like batch processing.
    """
    
    def __init__(self, name: str):
        self.name = name
        self._is_initialized = False
    
    def synthesize(self, text: str, output_path: str, **kwargs) -> str:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            **kwargs: Engine-specific options
            
        Returns:
            Path to generated audio file
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement synthesize()")
    
    def synthesize_batch(
        self,
        texts: List[str],
        output_dir: str,
        filename_prefix: str = "output",
        **kwargs
    ) -> List[str]:
        """
        Default batch implementation - calls synthesize for each text.
        Subclasses can override for more efficient batch processing.
        """
        import os
        
        output_paths = []
        os.makedirs(output_dir, exist_ok=True)
        
        for i, text in enumerate(texts):
            output_path = os.path.join(
                output_dir,
                f"{filename_prefix}_{i+1:03d}.wav"
            )
            path = self.synthesize(text, output_path, **kwargs)
            output_paths.append(path)
        
        return output_paths


def create_engine(engine_type: str, **kwargs) -> TTSEngine:
    """
    Factory function to create TTS engine instances.
    
    Args:
        engine_type: One of 'xtts', 'edge', 'piper', 'kokoro'
        **kwargs: Engine-specific initialization parameters
        
    Returns:
        TTSEngine instance
        
    Raises:
        ValueError: If engine_type is not supported
        ImportError: If required dependencies are not installed
    """
    engine_type = engine_type.lower()
    
    if engine_type == "xtts":
        from .xtts import XTTSEngine
        return XTTSEngine(**kwargs)
    
    elif engine_type == "edge":
        from .edge import EdgeTTSEngine
        return EdgeTTSEngine(**kwargs)
    
    elif engine_type == "piper":
        from .piper import PiperTTSEngine
        return PiperTTSEngine(**kwargs)
    
    elif engine_type == "kokoro":
        from .kokoro import KokoroTTSEngine
        return KokoroTTSEngine(**kwargs)
    
    else:
        raise ValueError(
            f"Unknown engine type: {engine_type}. "
            f"Supported: xtts, edge, piper, kokoro"
        )


def list_engines() -> List[str]:
    """List all available engine types."""
    return ["xtts", "edge", "piper", "kokoro"]


# Backward compatibility - keep old imports working
# These will be deprecated in future versions
try:
    from .xtts import XTTSEngine as TTSEngine  # noqa
except ImportError:
    pass  # torch/TTS not installed

try:
    from .edge import EdgeTTSEngine  # noqa
except ImportError:
    pass  # edge-tts not installed

try:
    from .piper import PiperTTSEngine  # noqa
except ImportError:
    pass  # piper-tts not installed
