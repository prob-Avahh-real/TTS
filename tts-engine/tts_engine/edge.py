"""
Edge-TTS Engine Module - Cloud-based TTS via Microsoft Azure

Requires: edge-tts>=6.1.0
Network: Required
Local Model Size: 0MB (cloud service)
"""

import os
import asyncio
from typing import Optional, List
from pathlib import Path

from . import BaseTTSEngine


class EdgeTTSEngine(BaseTTSEngine):
    """
    Edge-TTS Engine using Microsoft Azure cloud service.
    
    No local models required, high quality synthesis.
    Requires internet connection.
    """
    
    # Backward compatibility attributes
    model_type = "edge"
    engine_type = "edge"
    
    def __init__(self):
        """Initialize Edge-TTS Engine."""
        super().__init__("edge")
        
        # Verify dependency is available
        try:
            import edge_tts
            self._edge_tts = edge_tts
        except ImportError as e:
            raise ImportError(
                "Edge-TTS not installed. Run: pip install edge-tts"
            ) from e
        
        print("✅ Edge-TTS - 0MB local model, high quality, requires network")
        self._is_initialized = True
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        language: str = "zh"
    ) -> str:
        """
        Synthesize speech using Edge-TTS.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            voice: Voice name (e.g., 'zh-CN-XiaoxiaoNeural')
            language: Language code for voice selection fallback
            
        Returns:
            Path to generated audio file
        """
        return self._synthesize_edge(text, output_path, voice, language)
    
    def _synthesize_edge(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        language: str = "zh"
    ) -> str:
        """
        Synthesize speech using Edge-TTS.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            voice: Voice name (e.g., 'zh-CN-XiaoxiaoNeural')
            language: Language code for voice selection fallback
            
        Returns:
            Path to generated audio file
        """
        # Default voice mapping
        if voice is None:
            voice_options = {
                "zh": "zh-CN-XiaoxiaoNeural",
                "en": "en-US-AriaNeural"
            }
            voice = voice_options.get(language, "zh-CN-XiaoxiaoNeural")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Async synthesis
        async def _async_synthesize():
            communicate = self._edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
        
        asyncio.run(_async_synthesize())
        print(f"Edge-TTS synthesis complete: {output_path}")
        return output_path
    
    def list_voices(self, language: str = "zh") -> List[str]:
        """
        List available voices for a language.
        
        Args:
            language: Language code (e.g., 'zh', 'en')
            
        Returns:
            List of voice names
        """
        async def _list_voices():
            voices = await self._edge_tts.list_voices()
            return [v["ShortName"] for v in voices if language in v["Locale"]]
        
        return asyncio.run(_list_voices())
    
    def synthesize_batch(
        self,
        texts: List[str],
        output_dir: str,
        voice: Optional[str] = None,
        language: str = "zh",
        filename_prefix: str = "output"
    ) -> List[str]:
        """
        Batch synthesis optimized for Edge-TTS.
        
        Note: Edge-TTS is network-bound, so parallel processing
        may not provide significant speedup.
        """
        # Default voice
        if voice is None:
            voice_options = {"zh": "zh-CN-XiaoxiaoNeural", "en": "en-US-AriaNeural"}
            voice = voice_options.get(language, "zh-CN-XiaoxiaoNeural")
        
        return super().synthesize_batch(
            texts=texts,
            output_dir=output_dir,
            voice=voice,
            language=language,
            filename_prefix=filename_prefix
        )
