"""
XTTS Engine Module - Heavy local model TTS

Requires: TTS>=0.22.0, torch>=2.0.0
Model Size: ~1.8GB
"""

import os
from typing import Optional, List, Union

# Import at module level for testability
import torch
from TTS.api import TTS

from . import BaseTTSEngine


class XTTSEngine(BaseTTSEngine):
    """
    XTTS-v2 TTS Engine supporting voice cloning and multiple speakers.
    
    This is a heavy model requiring significant GPU/CPU resources.
    """
    
    def __init__(
        self,
        model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
        device: Optional[str] = None,
        gpu: bool = True
    ):
        """
        Initialize XTTS Engine.
        
        Args:
            model_name: TTS model name (default XTTS-v2)
            device: 'cuda' or 'cpu', auto-detected if None
            gpu: Prefer GPU if available
        """
        super().__init__("xtts")
        
        # Auto-select device
        if device is None:
            if gpu and torch.cuda.is_available():
                self.device = "cuda"
            else:
                self.device = "cpu"
        else:
            self.device = device
        
        print(f"Loading XTTS model: {model_name}")
        print(f"Using device: {self.device}")
        
        # Initialize TTS model
        self.tts = TTS(model_name=model_name).to(self.device)
        self.model_name = model_name
        
        # Get available speakers
        self.speakers = self._get_available_speakers()
        self._is_initialized = True
    
    def _get_available_speakers(self) -> List[str]:
        """Get list of supported speakers from model."""
        try:
            if hasattr(self.tts, 'speakers') and self.tts.speakers:
                return list(self.tts.speakers)
            return []
        except:
            return []
    
    def synthesize(
        self,
        text: str,
        output_path: str,
        speaker_wav: Optional[str] = None,
        speaker_idx: Optional[Union[int, str]] = None,
        language: str = "zh"
    ) -> str:
        """
        Synthesize speech using XTTS.
        
        Args:
            text: Text to synthesize
            output_path: Output audio file path
            speaker_wav: Reference audio for voice cloning
            speaker_idx: Predefined speaker name/index
            language: Language code (e.g., 'zh', 'en')
            
        Returns:
            Path to generated audio file
            
        Raises:
            ValueError: If both speaker_wav and speaker_idx specified
        """
        if speaker_wav and speaker_idx:
            raise ValueError(
                "Cannot specify both speaker_wav and speaker_idx. Choose one."
            )
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # XTTS-specific synthesis
        if speaker_wav:
            # Voice cloning mode
            print(f"Voice cloning mode, reference: {speaker_wav}")
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_path
            )
        elif speaker_idx is not None:
            # Use predefined speaker
            print(f"Using predefined speaker: {speaker_idx}")
            self.tts.tts_to_file(
                text=text,
                speaker_idx=speaker_idx,
                language=language,
                file_path=output_path
            )
        else:
            # Default to first available speaker
            if self.speakers:
                speaker_idx = self.speakers[0]
                print(f"No speaker specified, using default: {speaker_idx}")
                self.tts.tts_to_file(
                    text=text,
                    speaker_idx=speaker_idx,
                    language=language,
                    file_path=output_path
                )
            else:
                raise ValueError("Please provide speaker_wav or speaker_idx")
        
        print(f"Synthesis complete: {output_path}")
        return output_path
    
    def clone_voice(
        self,
        text: str,
        reference_audio: str,
        output_path: str,
        language: str = "zh"
    ) -> str:
        """
        Clone voice using reference audio.
        
        Args:
            text: Text to synthesize
            reference_audio: Reference audio file path (20-60s recommended)
            output_path: Output audio file path
            language: Language code
            
        Returns:
            Path to generated audio file
        """
        return self.synthesize(
            text=text,
            output_path=output_path,
            speaker_wav=reference_audio,
            language=language
        )
    
    def list_speakers(self) -> List[str]:
        """Return list of available predefined speakers."""
        return self.speakers
