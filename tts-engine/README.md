# TTS Engine - 语音区分引擎

一个基于 Python 的文本转语音（TTS）引擎，专门用于语音区分和多说话者语音合成。

## 功能特性

- 🎤 **多说话者支持**：支持使用不同的预定义说话者进行语音合成
- 🎭 **语音克隆**：通过参考音频克隆任意说话者的声音
- 🌍 **多语言支持**：支持中文、英文等多种语言
- 📦 **批量处理**：支持批量文本转语音
- 🚀 **易于使用**：简洁的 API 接口，快速上手

## 安装

### 1. 克隆或下载项目

```bash
cd tts-engine
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：首次运行时会自动下载 TTS 模型（约 1-2 GB），请确保网络连接正常。

## 快速开始

### 基础使用

```python
from tts_engine import TTSEngine

# 初始化引擎
engine = TTSEngine()

# 合成语音
engine.synthesize(
    text="你好，这是一个测试。",
    output_path="output.wav",
    language="zh"
)
```

### 新推荐用法（工厂模式）⭐

```python
from tts_engine import create_engine

# 通过工厂函数创建引擎（推荐）
engine = create_engine("edge")  # 或 "xtts", "piper", "kokoro"

engine.synthesize(
    text="你好，这是使用工厂模式创建的引擎。",
    output_path="output.wav",
    language="zh"
)
```

**支持的引擎类型：**
- `"xtts"` - XTTS-v2（重型，1.8GB，支持语音克隆）
- `"edge"` - Edge-TTS（云端，0MB，需网络）✅ 推荐
- `"piper"` - Piper TTS（轻量，25-60MB，离线）
- `"kokoro"` - Kokoro TTS（轻量，82MB）

### 使用预定义说话者

```python
# 列出可用说话者
speakers = engine.list_speakers()
print(f"可用说话者: {speakers}")

# 使用特定说话者
engine.synthesize(
    text="这是使用特定说话者生成的语音。",
    output_path="output_speaker.wav",
    speaker_idx=speakers[0],  # 使用第一个说话者
    language="zh"
)
```

### 语音克隆

```python
# 使用参考音频克隆语音
engine.clone_voice(
    text="这是使用语音克隆生成的语音。",
    reference_audio="reference_speaker.wav",  # 参考音频（建议20-60秒）
    output_path="output_cloned.wav",
    language="zh"
)
```

### 批量合成

```python
texts = [
    "第一段文本。",
    "第二段文本。",
    "第三段文本。"
]

output_paths = engine.synthesize_batch(
    texts=texts,
    output_dir="outputs",
    language="zh"
)
```

## 运行示例

### 基础示例（XTTS-v2）

```bash
python example.py
```

示例代码展示了各种使用场景，包括：
- 基础语音合成
- 多说话者语音合成
- 语音克隆
- 批量处理
- 语音区分应用场景

### 运行测试

#### 单元测试（含功能级模拟）

```bash
# 运行所有单元 + 功能（mock）测试
python -m unittest discover tests

# 或使用测试运行脚本
python tests/run_tests.py

# 运行特定测试文件
python -m unittest tests.test_tts_engine
python -m unittest tests.test_lightweight_engine
python -m unittest tests.functional.test_edge_functional
python -m unittest tests.functional.test_xtts_functional
```

#### 集成测试和演示（实际调用）

```bash
# 完整集成测试（Edge-TTS 实测）
python test_lightweight_models.py

# Edge-TTS 演示
python demo_edge_tts.py
```

**测试前请先安装依赖：**
```bash
# Edge-TTS（推荐，已测试通过）
pip install edge-tts

# 如果遇到SSL问题
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org edge-tts
```

## API 文档

### TTSEngine 类

#### `__init__(model_name, device, gpu)`

初始化 TTS 引擎。

**参数：**
- `model_name` (str): TTS 模型名称，默认为 `"tts_models/multilingual/multi-dataset/xtts_v2"`
- `device` (str, optional): 指定设备（'cuda' 或 'cpu'），如果为 None 则自动选择
- `gpu` (bool): 是否优先使用 GPU，默认为 True

#### `synthesize(text, output_path, speaker_wav, speaker_idx, language)`

合成语音。

**参数：**
- `text` (str): 要合成的文本
- `output_path` (str): 输出音频文件路径
- `speaker_wav` (str, optional): 参考说话者音频文件路径（用于语音克隆）
- `speaker_idx` (int/str, optional): 说话者索引或名称（使用预定义说话者）
- `language` (str): 语言代码（如 'zh', 'en', 'en-US'），默认为 'zh'

**返回：** 输出文件路径

#### `clone_voice(text, reference_audio, output_path, language)`

语音克隆：使用参考音频克隆说话者的声音。

**参数：**
- `text` (str): 要合成的文本
- `reference_audio` (str): 参考音频文件路径（建议20-60秒，清晰无噪音）
- `output_path` (str): 输出音频文件路径
- `language` (str): 语言代码，默认为 'zh'

**返回：** 输出文件路径

#### `synthesize_batch(texts, output_dir, speaker_wav, speaker_idx, language, filename_prefix)`

批量合成语音。

**参数：**
- `texts` (List[str]): 文本列表
- `output_dir` (str): 输出目录
- `speaker_wav` (str, optional): 参考说话者音频文件路径
- `speaker_idx` (int/str, optional): 说话者索引或名称
- `language` (str): 语言代码，默认为 'zh'
- `filename_prefix` (str): 文件名前缀，默认为 'output'

**返回：** 输出文件路径列表

#### `list_speakers()`

列出所有可用的说话者。

**返回：** 说话者列表

## 支持的模型

### 默认模型：XTTS-v2（重型）

默认使用 **XTTS-v2** 模型，支持：
- 多说话者语音合成
- 语音克隆（零样本）
- 多语言支持（约16种语言）

**注意**：XTTS-v2 模型较大（1.8 GB），推理较慢。如需轻量级方案，请查看下方。

### 轻量级替代方案 ⭐推荐

我们提供了轻量级模型支持：

1. **Edge-TTS**（Microsoft云端）✅ 已测试通过
   - 模型大小：0 MB（云端服务）
   - 推理速度：<1秒
   - 高质量语音
   - 需要网络连接
   - 安装：`pip install edge-tts`

2. **Piper TTS**（离线方案）
   - 模型大小：25-60 MB（超轻量！）
   - 推理速度：<0.5秒（CPU实时）
   - 支持离线运行
   - 商业友好（MIT许可证）
   - 需要下载模型文件

**使用轻量级引擎（新推荐）：**
```python
from tts_engine import create_engine

# 创建 Edge-TTS 引擎（云端，0MB）
engine = create_engine("edge")

engine.synthesize(
    text="你好，这是测试。",
    output_path="output.wav",
    language="zh"
)
```

**旧版兼容用法（仍支持，但已弃用）：**
```python
from tts_engine_lightweight import EdgeTTSEngine

engine = EdgeTTSEngine()
engine.synthesize(
    text="你好，这是测试。",
    output_path="output.wav",
    language="zh"
)
```

详细对比请查看 `MODEL_COMPARISON.md`

## 语言代码

常用语言代码：
- `zh` 或 `zh-CN`: 中文（简体）
- `en` 或 `en-US`: 英语（美式）
- `en-GB`: 英语（英式）
- `es`: 西班牙语
- `fr`: 法语
- `de`: 德语
- `ja`: 日语
- `ko`: 韩语

## 注意事项

1. **首次运行**：首次运行时会自动下载模型文件（约 1-2 GB），请确保网络连接正常。
2. **GPU 支持**：如果有 NVIDIA GPU，建议安装 CUDA 版本的 PyTorch 以加速推理。
3. **参考音频**：用于语音克隆的参考音频建议：
   - 时长：20-60 秒
   - 质量：清晰无噪音
   - 格式：WAV 格式（推荐）
4. **内存要求**：建议至少 4GB 可用内存。

## 应用场景

- 📢 **内容创作**：为视频、播客等生成不同角色的语音
- 🎮 **游戏开发**：为游戏角色生成多样化语音
- 📚 **有声读物**：为不同角色使用不同声音
- 🎯 **个性化应用**：根据用户偏好选择不同声音
- 🌐 **多语言应用**：支持多语言语音合成

## 故障排除

### 问题：模型下载失败
**解决方案**：检查网络连接，或手动下载模型到缓存目录。

### 问题：GPU 不可用
**解决方案**：确保安装了 CUDA 版本的 PyTorch，或使用 CPU 模式（设置 `gpu=False`）。

### 问题：语音克隆效果不佳
**解决方案**：
- 使用更长的参考音频（30-60秒）
- 确保参考音频清晰无噪音
- 尝试不同的参考音频

## 许可证

本项目使用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 参考资源

- [Coqui TTS 文档](https://docs.coqui.ai/)
- [XTTS-v2 模型说明](https://docs.coqui.ai/en/latest/models/xtts.html)
