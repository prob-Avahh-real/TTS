#!/bin/bash
# 轻量级TTS模型测试脚本

echo "=========================================="
echo "轻量级TTS模型测试脚本"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装"
    exit 1
fi

echo "Python 版本: $(python --version)"
echo ""

# 创建输出目录
mkdir -p outputs

# 测试 Edge-TTS
echo "=========================================="
echo "测试 Edge-TTS"
echo "=========================================="
if python -c "import edge_tts" 2>/dev/null; then
    echo "✅ Edge-TTS 已安装"
    python demo_edge_tts.py
else
    echo "❌ Edge-TTS 未安装"
    echo ""
    echo "安装命令:"
    echo "  pip install edge-tts"
    echo ""
    echo "如果遇到SSL问题:"
    echo "  pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org edge-tts"
fi

echo ""
echo ""

# 注意：Piper TTS 需要下载模型文件，暂未包含在测试中
# 如需测试 Piper TTS，请：
# 1. 安装: pip install piper-tts
# 2. 下载模型: https://github.com/rhasspy/piper/releases
# 3. 使用 piper 命令行工具测试

echo ""
echo ""

# 运行完整测试
echo "=========================================="
echo "运行完整测试套件"
echo "=========================================="
python test_lightweight_models.py

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="
