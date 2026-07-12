# 单元测试说明

## 测试结构

```
tests/
├── __init__.py
├── conftest.py                      # 统一mock依赖
├── functional/                     # 功能/集成测试（mock，无需网络）
│   ├── __init__.py
│   ├── test_edge_functional.py     # Edge-TTS 管线（模拟）
│   └── test_xtts_functional.py     # XTTS 管线（模拟）
├── integration/                    # 真实集成测试（需要网络）
│   ├── __init__.py
│   ├── live/                        # live 集成测试（真实网络）
│   │   ├── __init__.py
│   │   ├── test_edge_live.py        # Edge-TTS 真实调用
│   │   └── test_xtts_live.py        # XTTS 真实调用（默认跳过）
│   ├── run_integration_tests.py    # 集成测试运行脚本
│   └── README.md                   # 集成测试说明
├── test_tts_engine.py              # TTSEngine 单元测试
├── test_lightweight_engine.py       # 轻量级引擎单元测试
├── test_utils.py                   # 工具函数测试
├── run_tests.py                    # 单元测试运行脚本
└── TEST_SUMMARY.md                 # 测试摘要
```

## 运行测试

### 方法1：使用unittest（推荐）

```bash
# 运行所有测试
python -m unittest discover tests

# 运行特定测试文件
python -m unittest tests.test_tts_engine
python -m unittest tests.test_lightweight_engine
python -m unittest tests.test_utils

# 运行特定测试类
python -m unittest tests.test_tts_engine.TestTTSEngine

# 运行特定测试方法
python -m unittest tests.test_tts_engine.TestTTSEngine.test_init_default
```

### 方法2：使用测试运行脚本

```bash
# 运行单元测试（mock，快速）
python tests/run_tests.py

# 运行集成测试（真实网络调用）
python tests/integration/run_integration_tests.py
```

### 方法3：使用pytest（如果已安装）

```bash
# 安装pytest
pip install pytest

# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_tts_engine.py

# 显示详细输出
pytest -v tests/
```

## 测试覆盖

### test_tts_engine.py
- ✅ 引擎初始化（默认、GPU、自定义设备）
- ✅ 列出说话者
- ✅ 语音合成（speaker_idx、speaker_wav）
- ✅ 语音克隆
- ✅ 批量合成
- ✅ 错误处理（冲突参数）

### test_lightweight_engine.py
- ✅ Edge-TTS引擎初始化
- ✅ Edge-TTS列出语音
- ✅ Edge-TTS合成
- ✅ Piper TTS引擎初始化
- ✅ Piper TTS合成
- ✅ 批量合成

### test_utils.py
- ✅ 输出目录创建
- ✅ 文件路径验证

### 功能/集成（模拟，无需真实网络）
- `tests.functional.test_edge_functional.py`：Edge-TTS 管线写文件
- `tests.functional.test_xtts_functional.py`：XTTS 管线写文件

### 真实集成测试（需要网络）
- `tests.integration.live.test_edge_live.py`：Edge-TTS 真实调用
- `tests.integration.live.test_xtts_live.py`：XTTS 真实调用（默认跳过）

## 当前状态

- **单元测试**：21/21 全部通过 ✅
  - 单元：19 个
  - 功能/集成（模拟）：2 个

- **集成测试**：需要网络和实际依赖
  - Edge-TTS：5个测试（需要网络）
  - XTTS：默认跳过（需要大模型）

## 注意事项

1. **Mock依赖**：测试使用unittest.mock模拟外部依赖（TTS库、torch等），避免实际加载大型模型
2. **临时文件**：测试会自动创建和清理临时目录
3. **异步测试**：Edge-TTS测试需要处理异步函数，使用asyncio.run()
4. **跳过测试**：如果某些依赖未安装，相关测试会被跳过

## 添加新测试

1. 在对应的测试文件中添加新的测试方法
2. 测试方法名必须以`test_`开头
3. 使用`unittest.TestCase`的断言方法
4. 使用`setUp()`和`tearDown()`管理测试资源

示例：
```python
def test_new_feature(self):
    """测试新功能"""
    # 准备测试数据
    # 执行测试
    # 验证结果
    self.assertEqual(actual, expected)
```
