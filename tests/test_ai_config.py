#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI配置功能
"""

import sys
import os
from pathlib import Path

# 添加父目录到Python路径以导入主项目模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from weekly_task import WeeklyTaskManager

def test_ai_config():
    """测试AI配置功能"""
    print("🧪 测试AI配置功能")
    print("=" * 50)
    
    # 测试1: 从settings.xml读取配置
    print("📋 测试1: 从settings.xml读取配置")
    task_manager = WeeklyTaskManager()
    
    print(f"API Key: {'已配置' if task_manager.api_key else '未配置'}")
    print(f"Base URL: {task_manager.base_url}")
    print(f"客户端状态: {'已初始化' if task_manager.client else '未初始化'}")
    
    # 测试2: 读取设置方法
    print("\n📋 测试2: 读取XML设置")
    settings = task_manager.load_settings_from_xml()
    print(f"AI设置: {settings}")
    
    # 测试3: 手动设置API密钥
    print("\n📋 测试3: 手动设置API密钥")
    test_manager = WeeklyTaskManager(
        api_key="test-key",
        base_url="https://test.example.com"
    )
    print(f"手动设置 - API Key: {test_manager.api_key}")
    print(f"手动设置 - Base URL: {test_manager.base_url}")
    
    print("\n✅ 测试完成！")

if __name__ == "__main__":
    test_ai_config()
