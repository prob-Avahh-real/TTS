# 项目结构

## 📁 文件说明

### 核心代码
- `tts_engine.py` - XTTS-v2引擎（支持语音克隆）
- `tts_engine_lightweight.py` - 轻量级引擎（Edge-TTS封装）

### 示例和测试
- `example.py` - XTTS-v2使用示例
- `demo_edge_tts.py` - Edge-TTS演示脚本
- `test_lightweight_models.py` - 完整测试套件
- `run_tests.sh` - 自动化测试脚本

### 文档
- `README.md` - 项目主文档
- `MODEL_COMPARISON.md` - 模型详细对比说明
- `PROJECT_STRUCTURE.md` - 项目结构说明
- `tests/README.md` - 测试说明
- `tests/TEST_SUMMARY.md` - 测试摘要

### 配置
- `requirements.txt` - Python依赖
- `.gitignore` - Git忽略配置

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行示例 / 测试
python example.py                    # XTTS-v2示例
python demo_edge_tts.py              # Edge-TTS演示
python test_lightweight_models.py    # 完整测试（集成）
python tests/run_tests.py            # 单元+功能测试（mock，无需网络）

# 或使用shell脚本
./run_tests.sh
```

## 📊 模型选择

- **需要语音克隆** → 使用 `tts_engine.py` (XTTS-v2)
- **需要轻量级+云端** → 使用 `tts_engine_lightweight.py` (Edge-TTS)
- **需要离线** → 使用 Piper TTS（需要下载模型）

详细对比见 `MODEL_COMPARISON.md`
