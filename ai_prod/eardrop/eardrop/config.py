"""
Configuration settings for eardrop
"""

class Config:
    """Default configuration for audio processing"""
    
    # Audio processing settings
    DEFAULT_SAMPLE_RATE = 22050  # Hz
    HOP_LENGTH = 512
    N_FFT = 2048
    
    # Feature extraction settings
    N_MFCC = 13  # Number of MFCC coefficients
    N_MELS = 128  # Number of mel bands
    
    # Analysis settings
    SIMILARITY_THRESHOLD = 0.8
    
    # Supported audio formats
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
