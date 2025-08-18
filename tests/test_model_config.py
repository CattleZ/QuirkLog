#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试模型配置功能
"""

import sys
import os
from pathlib import Path

# 添加父目录到Python路径以导入主项目模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from weekly_task import WeeklyTaskManager

def test_model_config():
    """测试模型配置功能"""
    print("🧪 测试模型配置功能")
    print("=" * 50)
    
    # 测试1: 从settings.xml读取模型配置
    print("📋 测试1: 从settings.xml读取模型配置")
    task_manager = WeeklyTaskManager()
    
    print(f"默认模型: {task_manager.model}")
    print(f"API Key: {'已配置' if task_manager.api_key else '未配置'}")
    print(f"Base URL: {task_manager.base_url}")
    print(f"客户端状态: {'已初始化' if task_manager.client else '未初始化'}")
    
    # 测试2: 读取设置方法
    print("\n📋 测试2: 读取XML设置")
    settings = task_manager.load_settings_from_xml()
    print(f"读取到的设置:")
    for key, value in settings.items():
        if key == 'openrouterApiKey' and value:
            print(f"  {key}: {'*' * 20}...{value[-8:]}")  # 隐藏API密钥
        else:
            print(f"  {key}: {value}")
    
    # 测试3: 手动设置不同模型
    print("\n📋 测试3: 手动设置不同模型")
    test_models = [
        "gpt-3.5-turbo",
        "claude-3-haiku",
        "gemini-flash-1.5"
    ]
    
    for model in test_models:
        test_manager = WeeklyTaskManager(
            api_key="test-key",
            base_url="https://test.example.com",
            model=model
        )
        print(f"  设置模型 {model}: {'成功' if test_manager.model == model else '失败'}")
    
    # 测试4: 模型优先级测试
    print("\n📋 测试4: 模型配置优先级测试")
    
    # 参数优先级最高
    priority_manager = WeeklyTaskManager(model="priority-test-model")
    print(f"  参数优先级: {priority_manager.model}")
    
    # XML配置次优先级
    xml_manager = WeeklyTaskManager()
    print(f"  XML配置: {xml_manager.model}")
    
    print("\n✅ 模型配置测试完成！")

if __name__ == "__main__":
    test_model_config()
