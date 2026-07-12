# Eardrop - TTS Audio Differentiation Tool

Eardrop 是一个用于 TTS（文本转语音）音频差异化分析的 Python 工具。

## 功能特性

- 支持多种音频格式（WAV, MP3, FLAC 等）
- 音频特征提取（MFCC、频谱特征、音调特征等）
- 音频差异化分析和对比
- 可视化工具

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

## 项目结构

```
eardrop/
├── eardrop/          # 主模块
│   ├── core/         # 核心功能模块
│   └── utils/        # 工具模块
├── tests/            # 测试文件
└── main.py           # 主入口文件
```

## 依赖

- librosa - 音频分析和特征提取
- numpy - 数值计算
- scipy - 科学计算
- soundfile - 音频文件读写
- matplotlib - 可视化
