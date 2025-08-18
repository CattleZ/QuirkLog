#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 测试运行器
批量运行所有测试脚本
"""

import subprocess
import sys
from pathlib import Path
import glob

def run_tests():
    """运行所有测试脚本"""
    print("🧪 QuirkLog 测试套件")
    print("=" * 50)
    
    # 确保在正确的目录
    project_root = Path(__file__).parent
    if not (project_root / "weekly_task.py").exists():
        print("❌ 错误：请在QuirkLog项目根目录运行此脚本")
        print(f"   当前目录: {project_root}")
        print(f"   期望文件: weekly_task.py")
        return False
    
    # 查找所有测试文件
    test_files = sorted(glob.glob(str(project_root / "tests" / "test_*.py")))
    
    if not test_files:
        print("❌ 未找到测试文件")
        return False
    
    print(f"📋 找到 {len(test_files)} 个测试文件")
    print()
    
    results = []
    
    for test_file in test_files:
        test_name = Path(test_file).name
        print(f"🔄 运行测试: {test_name}")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                [sys.executable, test_file],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=60  # 60秒超时
            )
            
            if result.returncode == 0:
                print("✅ 测试通过")
                results.append((test_name, True, ""))
                if result.stdout.strip():
                    print(result.stdout)
            else:
                print("❌ 测试失败")
                results.append((test_name, False, result.stderr))
                if result.stdout.strip():
                    print("输出:", result.stdout)
                if result.stderr.strip():
                    print("错误:", result.stderr)
                    
        except subprocess.TimeoutExpired:
            print("⏰ 测试超时")
            results.append((test_name, False, "测试执行超时"))
        except Exception as e:
            print(f"💥 测试异常: {e}")
            results.append((test_name, False, str(e)))
        
        print()
    
    # 输出总结
    print("=" * 50)
    print("📊 测试结果总结")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, error in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:<25} {status}")
        if not success and error:
            print(f"   错误: {error}")
    
    print()
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
        return True
    else:
        print("⚠️  部分测试失败，请检查上述错误信息")
        return False

def run_demo():
    """运行演示脚本"""
    print("\n🎭 运行AI功能演示")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    demo_file = project_root / "tests" / "demo_ai_config.py"
    
    if not demo_file.exists():
        print("❌ 演示文件不存在")
        return False
    
    try:
        subprocess.run([sys.executable, str(demo_file)], cwd=project_root)
        return True
    except Exception as e:
        print(f"❌ 演示运行失败: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="QuirkLog 测试运行器")
    parser.add_argument("--demo", action="store_true", help="运行演示脚本")
    parser.add_argument("--all", action="store_true", help="运行测试和演示")
    
    args = parser.parse_args()
    
    success = True
    
    if args.demo or args.all:
        success &= run_demo()
    else:
        success &= run_tests()
        
        if args.all and success:
            success &= run_demo()
    
    sys.exit(0 if success else 1)
