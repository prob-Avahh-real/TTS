# 集成测试说明

## 概述

集成测试是真实调用外部服务的测试，需要：
- ✅ 网络连接（Edge-TTS）
- ✅ 实际依赖库（edge-tts, torch, TTS等）
- ✅ 可能下载大型模型（XTTS-v2约1.8GB）

## 测试分类

### Edge-TTS 集成测试 ✅ 推荐运行

- **文件**: `live/test_edge_live.py`
- **依赖**: `edge-tts`（已安装）
- **网络**: 需要（Microsoft云端服务）
- **模型大小**: 0 MB（云端）
- **运行时间**: 快（<5秒）

**运行**:
```bash
# 运行Edge-TTS集成测试
python -m unittest tests.integration.live.test_edge_live

# 或使用pytest
pytest tests/integration/live/test_edge_live.py -v
```

### XTTS-v2 集成测试 ⚠️ 默认跳过

- **文件**: `live/test_xtts_live.py`
- **依赖**: `torch`, `TTS`（需要安装）
- **网络**: 需要（下载模型）
- **模型大小**: 约1.8 GB
- **运行时间**: 慢（首次需要下载模型）

**注意**: 默认标记为 `@unittest.skip`，因为：
- 模型太大（1.8GB）
- 下载时间长
- 需要大量内存

**手动运行**:
```bash
# 取消skip标记后运行
python -m unittest tests.integration.live.test_xtts_live
```

## 跳过机制

集成测试会自动跳过如果：
- ❌ 依赖未安装（`@unittest.skipUnless`）
- ❌ 网络不可用（Edge-TTS测试）
- ❌ 标记为skip（XTTS测试默认跳过）

## 运行所有集成测试

```bash
# 运行所有集成测试（会自动跳过不可用的）
python -m unittest discover tests/integration

# 只运行Edge-TTS集成测试
python -m unittest tests.integration.live.test_edge_live -v
```

## 与单元测试的区别

| 特性 | 单元测试 | 集成测试 |
|------|----------|----------|
| **依赖** | Mock | 真实依赖 |
| **网络** | 不需要 | 需要 |
| **速度** | 快（<1秒） | 慢（几秒到几分钟） |
| **模型** | 不加载 | 可能需要下载 |
| **用途** | 验证逻辑 | 验证真实调用 |

## CI/CD 建议

在CI/CD中：
- ✅ **总是运行**单元测试（快速、稳定）
- ✅ **可选运行**Edge-TTS集成测试（需要网络）
- ⚠️ **跳过**XTTS集成测试（除非专门测试）

示例：
```yaml
# GitHub Actions示例
- name: Run unit tests
  run: python tests/run_tests.py

- name: Run integration tests (optional)
  run: python -m unittest tests.integration.live.test_edge_live
  continue-on-error: true  # 网络问题不影响CI
```

## 故障排除

### Edge-TTS 测试失败

**问题**: `网络不可用`
- 检查网络连接
- 检查防火墙设置
- 测试会自动跳过

**问题**: `Edge-TTS 未安装`
```bash
pip install edge-tts
```

### XTTS 测试跳过

这是正常的，因为：
- 模型太大（1.8GB）
- 需要大量内存
- 下载时间长

如果需要测试，手动取消skip标记。
