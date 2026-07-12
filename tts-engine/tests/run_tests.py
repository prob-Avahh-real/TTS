"""
运行所有单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入conftest以设置mock（必须在导入被测试模块之前）
import tests.conftest  # noqa


def run_all_tests():
    """运行所有测试"""
    # 发现并加载所有测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试模块
    test_modules = [
        # 单元测试
        'tests.test_tts_engine',
        'tests.test_lightweight_engine',
        'tests.test_utils',
        # 功能/集成测试（使用mock，无需真实网络）
        'tests.functional.test_edge_functional',
        'tests.functional.test_xtts_functional',
    ]
    
    for module_name in test_modules:
        try:
            tests = loader.loadTestsFromName(module_name)
            suite.addTests(tests)
            print(f"✅ 加载测试模块: {module_name}")
        except Exception as e:
            print(f"⚠️  无法加载测试模块 {module_name}: {e}")
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("运行单元测试")
    print("=" * 60)
    print()
    
    success = run_all_tests()
    
    print()
    print("=" * 60)
    if success:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
