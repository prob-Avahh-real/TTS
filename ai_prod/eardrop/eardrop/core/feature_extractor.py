"""
Audio feature extraction module
"""

import numpy as np
import librosa
from typing import Dict, Optional
from eardrop.config import Config


class FeatureExtractor:
    """Extract various audio features for analysis"""
    
    def __init__(self, sample_rate: int = None, n_mfcc: int = None, 
                 n_mels: int = None, n_fft: int = None, hop_length: int = None):
        """
        Initialize FeatureExtractor
        
        Args:
            sample_rate: Sample rate (default from Config)
            n_mfcc: Number of MFCC coefficients (default from Config)
            n_mels: Number of mel bands (default from Config)
            n_fft: FFT window size (default from Config)
            hop_length: Hop length (default from Config)
        """
        self.sample_rate = sample_rate or Config.DEFAULT_SAMPLE_RATE
        self.n_mfcc = n_mfcc or Config.N_MFCC
        self.n_mels = n_mels or Config.N_MELS
        self.n_fft = n_fft or Config.N_FFT
        self.hop_length = hop_length or Config.HOP_LENGTH
    
    def extract_mfcc(self, audio: np.ndarray, sr: Optional[int] = None) -> np.ndarray:
        """
        Extract MFCC (Mel-frequency cepstral coefficients) features
        
        Args:
            audio: Audio signal
            sr: Sample rate (if None, uses self.sample_rate)
            
        Returns:
            MFCC features matrix (n_mfcc, time_frames)
        """
        sr = sr or self.sample_rate
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        return mfccs
    
    def extract_spectral_features(self, audio: np.ndarray, sr: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Extract spectral features
        
        Args:
            audio: Audio signal
            sr: Sample rate (if None, uses self.sample_rate)
            
        Returns:
            Dictionary with spectral features
        """
        sr = sr or self.sample_rate
        
        # Compute short-time Fourier transform
        stft = librosa.stft(audio, n_fft=self.n_fft, hop_length=self.hop_length)
        magnitude = np.abs(stft)
        
        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )[0]
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )[0]
        
        # Spectral bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=audio, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length
        )[0]
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio, hop_length=self.hop_length)[0]
        
        return {
            'spectral_centroid': spectral_centroids,
            'spectral_rolloff': spectral_rolloff,
            'spectral_bandwidth': spectral_bandwidth,
            'zero_crossing_rate': zcr,
            'magnitude': magnitude
        }
    
    def extract_pitch_features(self, audio: np.ndarray, sr: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Extract pitch-related features
        
        Args:
            audio: Audio signal
            sr: Sample rate (if None, uses self.sample_rate)
            
        Returns:
            Dictionary with pitch features
        """
        sr = sr or self.sample_rate
        
        # Fundamental frequency (F0) using pyin
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr,
            hop_length=self.hop_length
        )
        
        return {
            'f0': f0,
            'voiced_flag': voiced_flag,
            'voiced_probs': voiced_probs
        }
    
    def extract_energy_features(self, audio: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Extract energy-related features
        
        Args:
            audio: Audio signal
            
        Returns:
            Dictionary with energy features
        """
        # RMS energy
        rms = librosa.feature.rms(y=audio, hop_length=self.hop_length)[0]
        
        # Energy envelope
        energy = np.abs(audio) ** 2
        
        return {
            'rms': rms,
            'energy': energy
        }
    
    def extract_all_features(self, audio: np.ndarray, sr: Optional[int] = None) -> Dict[str, np.ndarray]:
        """
        Extract all available features
        
        Args:
            audio: Audio signal
            sr: Sample rate (if None, uses self.sample_rate)
            
        Returns:
            Dictionary with all extracted features
        """
        features = {}
        
        # MFCC
        features['mfcc'] = self.extract_mfcc(audio, sr)
        
        # Spectral features
        spectral = self.extract_spectral_features(audio, sr)
        features.update(spectral)
        
        # Pitch features
        pitch = self.extract_pitch_features(audio, sr)
        features.update(pitch)
        
        # Energy features
        energy = self.extract_energy_features(audio)
        features.update(energy)
        
        return features
    
    def get_feature_vector(self, features: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Convert features to a single feature vector
        
        Args:
            features: Dictionary of features
            
        Returns:
            Flattened feature vector
        """
        feature_vectors = []
        
        for key, value in features.items():
            if value is not None:
                # Compute statistics for time-varying features
                if len(value.shape) > 1:
                    # Multi-dimensional features: take mean and std
                    feature_vectors.append(np.mean(value, axis=1))
                    feature_vectors.append(np.std(value, axis=1))
                elif len(value.shape) == 1:
                    # 1D features: take mean and std
                    feature_vectors.append(np.array([np.mean(value), np.std(value)]))
                else:
                    # Scalar features
                    feature_vectors.append(np.array([value]))
        
        return np.concatenate([v.flatten() for v in feature_vectors if v.size > 0])
