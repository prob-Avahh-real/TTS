"""
Audio loading and preprocessing module
"""

import os
import numpy as np
import librosa
import soundfile as sf
from typing import Optional, Tuple, Dict
from eardrop.config import Config


class AudioLoader:
    """Load and preprocess audio files"""
    
    def __init__(self, sample_rate: int = None, hop_length: int = None):
        """
        Initialize AudioLoader
        
        Args:
            sample_rate: Target sample rate (default from Config)
            hop_length: Hop length for frame analysis (default from Config)
        """
        self.sample_rate = sample_rate or Config.DEFAULT_SAMPLE_RATE
        self.hop_length = hop_length or Config.HOP_LENGTH
    
    def load_audio(self, file_path: str, sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file
        
        Args:
            file_path: Path to audio file
            sr: Sample rate (if None, uses self.sample_rate)
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Check file extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in Config.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported audio format: {ext}")
        
        target_sr = sr or self.sample_rate
        
        # Load audio using librosa
        audio, sr = librosa.load(file_path, sr=target_sr)
        
        return audio, sr
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio to [-1, 1] range
        
        Args:
            audio: Audio signal
            
        Returns:
            Normalized audio signal
        """
        if len(audio) == 0:
            return audio
        
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio
    
    def preprocess_audio(self, file_path: str, normalize: bool = True) -> Tuple[np.ndarray, int, Dict]:
        """
        Load and preprocess audio file
        
        Args:
            file_path: Path to audio file
            normalize: Whether to normalize audio
            
        Returns:
            Tuple of (audio_data, sample_rate, metadata)
        """
        audio, sr = self.load_audio(file_path)
        
        if normalize:
            audio = self.normalize_audio(audio)
        
        # Extract metadata
        metadata = self.get_metadata(file_path, audio, sr)
        
        return audio, sr, metadata
    
    def get_metadata(self, file_path: str, audio: np.ndarray, sr: int) -> Dict:
        """
        Extract audio metadata
        
        Args:
            file_path: Path to audio file
            audio: Audio signal
            sr: Sample rate
            
        Returns:
            Dictionary with metadata
        """
        duration = len(audio) / sr
        
        metadata = {
            'file_path': file_path,
            'duration': duration,
            'sample_rate': sr,
            'num_samples': len(audio),
            'channels': 1 if len(audio.shape) == 1 else audio.shape[1],
        }
        
        # Try to get additional metadata from soundfile
        try:
            info = sf.info(file_path)
            metadata.update({
                'format': info.format,
                'subtype': info.subtype,
                'frames': info.frames,
            })
        except Exception:
            pass
        
        return metadata
    
    def frame_audio(self, audio: np.ndarray, frame_length: int = None, 
                   hop_length: int = None) -> np.ndarray:
        """
        Split audio into frames
        
        Args:
            audio: Audio signal
            frame_length: Length of each frame in samples
            hop_length: Hop length between frames
            
        Returns:
            Array of frames
        """
        frame_length = frame_length or Config.N_FFT
        hop_length = hop_length or self.hop_length
        
        frames = librosa.util.frame(
            audio, 
            frame_length=frame_length, 
            hop_length=hop_length,
            axis=0
        )
        
        return frames
