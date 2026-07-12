"""
TTS引擎使用示例
演示如何使用TTS引擎进行语音合成和语音区分
"""

from tts_engine import TTSEngine


def example_basic_synthesis():
    """基础语音合成示例"""
    print("=" * 50)
    print("示例1: 基础语音合成")
    print("=" * 50)
    
    # 初始化引擎
    engine = TTSEngine()
    
    # 合成语音
    engine.synthesize(
        text="欢迎使用TTS引擎，这是一个支持语音区分的文本转语音系统。",
        output_path="outputs/example1_basic.wav",
        language="zh"
    )


def example_multi_speaker():
    """多说话者示例"""
    print("\n" + "=" * 50)
    print("示例2: 多说话者语音合成")
    print("=" * 50)
    
    engine = TTSEngine()
    
    # 列出可用说话者
    speakers = engine.list_speakers()
    if speakers:
        print(f"可用说话者: {speakers}")
        
        # 使用不同说话者合成相同文本
        text = "这是多说话者测试，每个说话者都有独特的声音特征。"
        
        for i, speaker in enumerate(speakers[:3]):  # 只使用前3个说话者
            output_path = f"outputs/example2_speaker_{i+1}.wav"
            engine.synthesize(
                text=text,
                output_path=output_path,
                speaker_idx=speaker,
                language="zh"
            )
            print(f"已生成: {output_path} (说话者: {speaker})")
    else:
        print("该模型不支持预定义说话者，请使用语音克隆模式")


def example_voice_cloning():
    """语音克隆示例"""
    print("\n" + "=" * 50)
    print("示例3: 语音克隆")
    print("=" * 50)
    
    engine = TTSEngine()
    
    # 参考音频路径（需要用户提供）
    reference_audio = "reference_audio.wav"  # 请替换为实际的参考音频路径
    
    import os
    if os.path.exists(reference_audio):
        # 使用参考音频克隆语音
        texts = [
            "这是第一段测试文本。",
            "这是第二段测试文本，用于验证语音克隆的一致性。",
            "这是第三段测试文本，展示语音克隆的效果。"
        ]
        
        for i, text in enumerate(texts):
            output_path = f"outputs/example3_cloned_{i+1}.wav"
            engine.clone_voice(
                text=text,
                reference_audio=reference_audio,
                output_path=output_path,
                language="zh"
            )
            print(f"已生成: {output_path}")
    else:
        print(f"参考音频文件不存在: {reference_audio}")
        print("请提供参考音频文件（建议20-60秒，清晰无噪音）")


def example_batch_synthesis():
    """批量合成示例"""
    print("\n" + "=" * 50)
    print("示例4: 批量语音合成")
    print("=" * 50)
    
    engine = TTSEngine()
    
    texts = [
        "第一段文本：今天天气真好。",
        "第二段文本：适合出去散步。",
        "第三段文本：享受美好的时光。"
    ]
    
    # 批量合成
    output_paths = engine.synthesize_batch(
        texts=texts,
        output_dir="outputs/batch",
        language="zh",
        filename_prefix="batch_output"
    )
    
    print(f"批量合成完成，共生成 {len(output_paths)} 个文件:")
    for path in output_paths:
        print(f"  - {path}")


def example_voice_differentiation():
    """语音区分示例：展示如何为不同场景使用不同声音"""
    print("\n" + "=" * 50)
    print("示例5: 语音区分应用场景")
    print("=" * 50)
    
    engine = TTSEngine()
    
    # 不同场景的文本和说话者配置
    scenarios = [
        {
            "name": "新闻播报",
            "text": "今日新闻：科技发展日新月异，人工智能技术不断突破。",
            "speaker_idx": None,  # 可以使用特定说话者
            "reference_audio": None  # 或使用参考音频
        },
        {
            "name": "故事讲述",
            "text": "从前有一座山，山上有一座庙，庙里有一个老和尚。",
            "speaker_idx": None,
            "reference_audio": None
        },
        {
            "name": "产品介绍",
            "text": "欢迎使用我们的TTS引擎，它支持多说话者和语音克隆功能。",
            "speaker_idx": None,
            "reference_audio": None
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        output_path = f"outputs/scenario_{i+1}_{scenario['name']}.wav"
        
        try:
            engine.synthesize(
                text=scenario["text"],
                output_path=output_path,
                speaker_idx=scenario["speaker_idx"],
                speaker_wav=scenario["reference_audio"],
                language="zh"
            )
            print(f"已生成场景 '{scenario['name']}': {output_path}")
        except Exception as e:
            print(f"生成场景 '{scenario['name']}' 时出错: {e}")


if __name__ == "__main__":
    # 创建输出目录
    import os
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("outputs/batch", exist_ok=True)
    
    # 运行示例
    try:
        example_basic_synthesis()
        example_multi_speaker()
        # example_voice_cloning()  # 需要参考音频文件
        example_batch_synthesis()
        example_voice_differentiation()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成！")
        print("=" * 50)
    except Exception as e:
        print(f"运行示例时出错: {e}")
        import traceback
        traceback.print_exc()
