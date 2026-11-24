# TTS

Python 多引擎语音合成与音频分析工作区：含 `tts-engine/`（Edge-TTS / Piper / Kokoro / XTTS-v2 工厂封装）及 `ai_prod/`（`eardrop` 音频特征对比、`go` 实验）。

## 用途与 Target 判定

| 平台 | 需要? | 方式 |
|------|-------|------|
| 移动端 | 不适用 | Python 语音合成引擎库与离线批处理工具 |
| 智能硬件 | 不适用 | 服务端/桌面音频合成管线，非穿戴固件 |

## 命令

```bash
cd tts-engine
pip install -r requirements.txt
bash run_tests.sh
```

## Harness / Loop（助手）

- 遵循根 `/Users/skat/AGENTS.md` Harness + Loop 规则
- Guide = 本文件；Sensor = `tts-engine/tests/` 与 `ai_prod/eardrop/tests/` pytest 套件
- 新增 TTS 后端统一走 `create_engine` 工厂接口；同类失误第二次沉淀测试（棘轮）

## 验证环 / Done

```bash
cd tts-engine && python3 -m pytest tests/
```

**Done 示例**：`tts-engine` 单元与轻量模型测试通过，工厂接口兼容既有语种与输出格式。
