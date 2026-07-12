"""
运行集成测试（真实网络调用）
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def run_integration_tests():
    """运行所有集成测试"""
    print("=" * 60)
    print("运行集成测试（真实网络调用）")
    print("=" * 60)
    print()
    print("⚠️  注意：集成测试需要网络连接和实际依赖")
    print("   如果依赖未安装或网络不可用，相关测试会被跳过")
    print()
    
    # 发现并加载集成测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加集成测试模块
    test_modules = [
        'tests.integration.live.test_edge_live',
        'tests.integration.live.test_xtts_live',
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
    
    # 统计
    print()
    print("=" * 60)
    print("集成测试结果统计")
    print("=" * 60)
    print(f"运行: {result.testsRun}")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.skipped:
        print("\n跳过的测试:")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    print("=" * 60)
    
    # 返回结果（跳过不算失败）
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_integration_tests()
    
    print()
    if success:
        print("✅ 所有可运行的集成测试通过！")
    else:
        print("❌ 部分集成测试失败")
    
    sys.exit(0 if success else 1)
