"""
Setup configuration for eardrop
"""

from setuptools import setup, find_packages

setup(
    name="eardrop",
    version="0.1.0",
    description="TTS Audio Differentiation Tool",
    packages=find_packages(),
    install_requires=[
        "librosa>=0.10.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "soundfile>=0.12.0",
        "matplotlib>=3.7.0",
        "pytest>=7.4.0",
    ],
    python_requires=">=3.8",
)
