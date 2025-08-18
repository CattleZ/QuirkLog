#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试定时任务功能
"""

import sys
import os

def test_without_api():
    """测试不使用真实API的定时任务功能"""
    print("🧪 测试定时任务功能（模拟模式）")
    print("=" * 40)
    
    # 模拟的AI响应
    mock_response = """
作为您的个人效率顾问，以下是本周的总结建议：

🔍 **每周回顾的重要性**
定期回顾帮助我们从经验中学习，调整方向，保持成长动力。

🤔 **自我反思问题**
1. 本周最大的成就是什么？
2. 遇到的主要挑战和学到的教训？
3. 哪些事情做得比预期更好？
4. 什么事情可以做得更好？
5. 本周的时间分配是否合理？

🎯 **下周目标设定建议**
- 设定2-3个具体、可衡量的目标
- 确保目标与长期愿景对齐
- 预留20%的时间处理意外情况

⏰ **时间管理技巧**
- 使用番茄工作法提高专注度
- 每天安排3个最重要的任务
- 定期回顾和调整优先级

💪 **保持动力的方法**
- 庆祝小的进步和成就
- 与支持的朋友分享目标
- 记录成长轨迹，看到进步

继续保持努力，每一天都是新的开始！ 🌟
    """.strip()
    
    # 模拟保存功能
    from datetime import datetime
    import json
    from pathlib import Path
    
    # 创建测试目录
    test_dir = Path("test_weekly_insights")
    test_dir.mkdir(exist_ok=True)
    
    # 生成测试文件
    now = datetime.now()
    filename = f"test_weekly_insight_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"
    file_path = test_dir / filename
    
    # 构建测试数据
    insight_data = {
        "date": now.strftime('%Y-%m-%d'),
        "timestamp": now.isoformat(),
        "week_number": now.isocalendar()[1],
        "year": now.year,
        "content": mock_response,
        "source": "Test Mode (Mock)",
        "model": "simulated"
    }
    
    # 保存测试文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(insight_data, f, ensure_ascii=False, indent=2)
    
    print("📝 模拟AI响应:")
    print(mock_response)
    print(f"\n💾 测试数据已保存到: {file_path}")
    print("✅ 测试完成")

def test_schedule_setup():
    """测试定时任务设置"""
    try:
        import schedule
        
        print("⏰ 测试定时任务设置...")
        
        # 清除现有任务
        schedule.clear()
        
        # 添加测试任务
        def test_job():
            print(f"🎯 测试任务执行 - {datetime.now()}")
        
        # 设置测试任务（每分钟执行一次，仅用于测试）
        schedule.every().minute.do(test_job)
        
        print("📅 已设置测试任务（每分钟执行）")
        print("🔧 任务列表:")
        for job in schedule.jobs:
            print(f"   - {job}")
        
        print("✅ 定时任务设置测试通过")
        
        # 清除测试任务
        schedule.clear()
        
    except ImportError:
        print("❌ schedule 模块未安装")
        print("请运行: pip install schedule")

def main():
    """主测试函数"""
    print("🧪 QuirkLog 定时任务测试套件")
    print("=" * 40)
    
    while True:
        print("\n选择测试:")
        print("1. 测试模拟AI响应和数据保存")
        print("2. 测试定时任务设置")
        print("3. 运行所有测试")
        print("4. 退出")
        
        choice = input("请选择 (1-4): ").strip()
        
        if choice == '1':
            test_without_api()
        elif choice == '2':
            test_schedule_setup()
        elif choice == '3':
            test_without_api()
            print("\n" + "-" * 20)
            test_schedule_setup()
        elif choice == '4':
            print("👋 测试结束")
            break
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()
