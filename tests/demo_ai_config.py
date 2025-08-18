#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog AI配置功能演示
展示完整的配置流程和功能验证
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import sys
import os

# 添加父目录到Python路径以导入主项目模块
sys.path.insert(0, str(Path(__file__).parent.parent))

def show_banner():
    """显示横幅"""
    print("🌟" + "=" * 58 + "🌟")
    print("🤖 QuirkLog AI智能助手配置功能演示")
    print("🌟" + "=" * 58 + "🌟")
    print()

def demonstrate_xml_config():
    """演示XML配置功能"""
    print("📋 1. XML配置文件结构演示")
    print("-" * 40)
    
    # 读取当前配置
    xml_file = Path('settings.xml')
    if xml_file.exists():
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # 检查AI设置
        ai_section = root.find('ai')
        if ai_section is not None:
            enabled = ai_section.find('enabled')
            api_key = ai_section.find('openrouterApiKey')
            base_url = ai_section.find('openrouterBaseUrl')
            
            print(f"✅ AI配置已存在")
            print(f"   启用状态: {enabled.text if enabled is not None else '未设置'}")
            print(f"   API密钥: {'已配置' if api_key is not None and api_key.text else '未配置'}")
            print(f"   服务地址: {base_url.text if base_url is not None else '未设置'}")
        else:
            print("❌ 未找到AI配置")
    else:
        print("❌ settings.xml文件不存在")
    
    print()

def demonstrate_weekly_task_integration():
    """演示每周任务集成"""
    print("🔄 2. 每周任务集成演示")
    print("-" * 40)
    
    try:
        from weekly_task import WeeklyTaskManager
        
        # 创建任务管理器
        manager = WeeklyTaskManager()
        
        print(f"✅ WeeklyTaskManager 已加载")
        print(f"   配置读取: {'成功' if hasattr(manager, 'load_settings_from_xml') else '失败'}")
        print(f"   API密钥: {'已配置' if manager.api_key else '未配置'}")
        print(f"   Base URL: {manager.base_url}")
        print(f"   客户端状态: {'已初始化' if manager.client else '未初始化'}")
        
        # 演示配置读取
        settings = manager.load_settings_from_xml()
        if settings:
            print(f"   读取到的设置: {json.dumps(settings, ensure_ascii=False, indent=2)}")
        else:
            print(f"   读取到的设置: 空配置")
            
    except ImportError as e:
        print(f"❌ 导入WeeklyTaskManager失败: {e}")
    except Exception as e:
        print(f"❌ 创建WeeklyTaskManager失败: {e}")
    
    print()

def demonstrate_web_integration():
    """演示Web集成"""
    print("🌐 3. Web界面集成演示")
    print("-" * 40)
    
    try:
        from web_server import SettingsHandler
        
        print("✅ SettingsHandler 已加载")
        
        # 检查相关方法
        handler = SettingsHandler(None, None, None)
        methods = [
            'handle_test_ai_connection',
            'test_openrouter_connection', 
            'update_settings_xml',
            'load_settings'
        ]
        
        for method in methods:
            if hasattr(handler, method):
                print(f"   ✅ {method}: 可用")
            else:
                print(f"   ❌ {method}: 不可用")
                
    except ImportError as e:
        print(f"❌ 导入SettingsHandler失败: {e}")
    except Exception as e:
        print(f"❌ 创建SettingsHandler失败: {e}")
    
    print()

def demonstrate_file_structure():
    """演示文件结构"""
    print("📁 4. 相关文件结构演示")
    print("-" * 40)
    
    important_files = [
        'weekly_task.py',
        'web_server.py', 
        'settings.xml',
        'index.html',
        'script.js',
        'style.css',
        'requirements.txt'
    ]
    
    for file_name in important_files:
        file_path = Path(file_name)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   ✅ {file_name}: {size} bytes")
        else:
            print(f"   ❌ {file_name}: 不存在")
    
    print()

def demonstrate_configuration_example():
    """演示配置示例"""
    print("⚙️ 5. 完整配置示例")
    print("-" * 40)
    
    example_settings = {
        "saveDirectory": "./downloads",
        "autoSave": True,
        "fileNaming": "每日记录_{date}",
        "aiEnabled": True,
        "openrouterApiKey": "sk-or-v1-xxxxxxxxxxxxxxxx",
        "openrouterBaseUrl": "https://openrouter.ai/api/v1"
    }
    
    print("JavaScript设置对象:")
    print(json.dumps(example_settings, ensure_ascii=False, indent=2))
    
    print("\n对应的XML结构:")
    print("""<settings>
    <general>
        <saveDirectory>./downloads</saveDirectory>
        <autoSave>true</autoSave>
    </general>
    <export>
        <fileNaming>每日记录_{date}</fileNaming>
    </export>
    <ai>
        <enabled>true</enabled>
        <openrouterApiKey>sk-or-v1-xxxxxxxxxxxxxxxx</openrouterApiKey>
        <openrouterBaseUrl>https://openrouter.ai/api/v1</openrouterBaseUrl>
    </ai>
</settings>""")
    
    print()

def show_usage_summary():
    """显示使用总结"""
    print("🎯 使用流程总结")
    print("-" * 40)
    print("1. 启动Web服务器: python web_server.py")
    print("2. 打开浏览器，点击⚙️设置按钮")  
    print("3. 在AI智能助手设置区域配置API密钥")
    print("4. 测试连接并保存设置")
    print("5. 启动AI功能: python main_launcher.py")
    print("6. 享受AI每周洞察功能！")
    print()

def main():
    """主函数"""
    show_banner()
    demonstrate_xml_config()
    demonstrate_weekly_task_integration()
    demonstrate_web_integration()
    demonstrate_file_structure()
    demonstrate_configuration_example()
    show_usage_summary()
    
    print("🌟" + "=" * 58 + "🌟")
    print("✨ AI配置功能演示完成！")
    print("📖 查看 AI_CONFIG_GUIDE.md 获取详细使用说明")
    print("🚀 查看 QUICK_AI_SETUP.md 获取快速配置指南")
    print("🌟" + "=" * 58 + "🌟")

if __name__ == "__main__":
    main()
