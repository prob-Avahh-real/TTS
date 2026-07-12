"""
Piper TTS Engine Module - Ultra-lightweight local TTS

Requires: piper-tts
Model Size: 25-60MB per voice
"""

import os
from typing import Optional, List

from . import BaseTTSEngine


class PiperTTSEngine(BaseTTSEngine):
    """
    Piper TTS Engine - ultra-lightweight local synthesis.
    
    Best for: Edge devices, real-time synthesis, offline use.
    Model size: 25-60MB per voice.
    """
    
    # Backward compatibility attributes
    model_type = "piper"
    engine_type = "piper"
    
    def __init__(self, voice: Optional[str] = None):
        """
        Initialize Piper TTS Engine.
        
        Args:
            voice: Default voice model name (e.g., 'zh_CN-xiaoyan-medium')
        """
        super().__init__("piper")
        
        # Verify dependency
        try:
            from piper import PiperVoice
            self._PiperVoice = PiperVoice
        except ImportError as e:
            raise ImportError(
                "Piper TTS not installed. Run: pip install piper-tts"
            ) from e
        
        self.default_voice = voice or "zh_CN-xiaoyan-medium"
        print("✅ Piper TTS - ultra-lightweight (25-60MB), CPU real-time, offline")
        self._is_initialized = True
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        language: str = "zh"
    ) -> str:
        """
        Synthesize speech using Piper TTS.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            voice: Voice model name (defaults to constructor value)
            language: Language code for voice selection fallback
            
        Returns:
            Path to generated audio file
        """
        return self._synthesize_piper(text, output_path, voice, language)
    
    def _synthesize_piper(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        language: str = "zh"
    ) -> str:
        """
        Synthesize speech using Piper TTS.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            voice: Voice model name (defaults to constructor value)
            language: Language code for voice selection fallback
            
        Returns:
            Path to generated audio file
        """
        # Select voice
        selected_voice = voice or self.default_voice
        
        # Default voice mapping if no voice specified
        if voice is None and language:
            voice_options = {
                "zh": "zh_CN-xiaoyan-medium",
                "en": "en_US-lessac-medium"
            }
            selected_voice = voice_options.get(language, self.default_voice)
        
        # Load voice model
        model_path = f"{selected_voice}.onnx"
        config_path = f"{selected_voice}.onnx.json"
        
        voice_model = self._PiperVoice.load(model_path, config_path=config_path)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Synthesize
        with open(output_path, "wb") as f:
            voice_model.synthesize(text, f)
        
        print(f"Piper TTS synthesis complete: {output_path}")
        return output_path
    
    def list_voices(self, language: str = "zh") -> List[str]:
        """
        List available voices.
        
        Note: This returns known voices. Actual availability depends
        on downloaded model files.
        """
        known_voices = [
            "zh_CN-xiaoyan-medium",
            "en_US-lessac-medium",
            "en_US-amy-medium",
        ]
        
        # Filter by language prefix
        return [v for v in known_voices if v.startswith(language)]
