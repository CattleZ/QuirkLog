#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 启动器 - 集成定时任务功能
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    missing_deps = []
    
    try:
        import schedule
    except ImportError:
        missing_deps.append('schedule')
    
    try:
        import openai
    except ImportError:
        missing_deps.append('openai')
    
    if missing_deps:
        print("❌ 缺少以下依赖包:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n💡 请运行以下命令安装依赖:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def run_main_app():
    """运行主应用程序"""
    print("🚀 启动主应用程序...")
    try:
        import launcher
        launcher.main()
    except ImportError:
        print("❌ 找不到主启动器模块")

def run_weekly_task():
    """运行定时任务"""
    print("⏰ 启动定时任务管理器...")
    try:
        import weekly_task
        weekly_task.main()
    except ImportError:
        print("❌ 找不到定时任务模块")

def show_menu():
    """显示主菜单"""
    print("🌟 QuirkLog 每日计划与总结应用程序")
    print("=" * 45)
    print("1. 🖥️  启动主应用程序")
    print("2. ⏰ 启动定时任务管理器")
    print("3. 📖 查看使用说明")
    print("4. 🔧 安装依赖")
    print("5. 🚪 退出")
    print("=" * 45)

def show_instructions():
    """显示使用说明"""
    print("\n📖 使用说明")
    print("=" * 30)
    print("主应用程序:")
    print("  - 每日计划管理和总结反思")
    print("  - Web界面和GUI界面")
    print("  - 数据保存和导出功能")
    print()
    print("定时任务:")
    print("  - 每周末自动执行AI洞察生成")
    print("  - 需要配置OpenRouter API密钥")
    print("  - 生成个人成长建议和计划指导")
    print()
    print("配置步骤:")
    print("  1. 复制 config_template.py 为 config.py")
    print("  2. 在 config.py 中填入您的API密钥")
    print("  3. 安装依赖: pip install -r requirements.txt")
    print("  4. 启动定时任务管理器")

def install_dependencies():
    """安装依赖"""
    print("🔧 安装依赖包...")
    import subprocess
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败，请手动运行: pip install -r requirements.txt")

def main():
    """主函数"""
    while True:
        print("\n")
        show_menu()
        
        choice = input("请选择 (1-5): ").strip()
        
        if choice == '1':
            if check_dependencies():
                run_main_app()
            else:
                print("请先安装依赖后再启动主应用程序")
        
        elif choice == '2':
            if check_dependencies():
                run_weekly_task()
            else:
                print("请先安装依赖后再启动定时任务")
        
        elif choice == '3':
            show_instructions()
        
        elif choice == '4':
            install_dependencies()
        
        elif choice == '5':
            print("👋 再见!")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()
