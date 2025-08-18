#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 智能启动器
自动检测和配置运行环境
"""

import sys
import os
import subprocess
import platform
import webbrowser
import time
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version >= (3, 7):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("💡 请升级到Python 3.7或更高版本")
        return False


def install_missing_modules():
    """安装缺失的模块"""
    print("🔍 检查依赖模块...")
    
    # 基础模块检查
    required_modules = {
        'tkinter': 'GUI界面支持',
        'http.server': 'Web服务器',
        'json': '数据处理',
        'xml.etree.ElementTree': '配置文件处理'
    }
    
    missing_modules = []
    
    for module, description in required_modules.items():
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'http.server':
                import http.server
            elif module == 'json':
                import json
            elif module == 'xml.etree.ElementTree':
                import xml.etree.ElementTree
            print(f"✅ {module} - {description}")
        except ImportError:
            missing_modules.append((module, description))
            print(f"❌ {module} - {description} (缺失)")
    
    # 尝试安装缺失的模块
    if missing_modules:
        print("\n📦 尝试安装缺失的模块...")
        for module, description in missing_modules:
            if module == 'tkinter':
                print("⚠️  tkinter需要手动安装:")
                if platform.system() == "Darwin":  # macOS
                    print("  brew install python-tk")
                elif platform.system() == "Linux":
                    print("  sudo apt-get install python3-tk")
                elif platform.system() == "Windows":
                    print("  tkinter通常随Python一起安装")
            else:
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", module
                    ], check=True, capture_output=True)
                    print(f"✅ 已安装 {module}")
                except subprocess.CalledProcessError:
                    print(f"❌ 安装 {module} 失败")
    
    return len(missing_modules) == 0


def auto_setup_environment():
    """自动设置运行环境"""
    print("⚙️  自动配置运行环境...")
    
    # 创建数据目录
    data_dir = Path.home() / "daylog"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 已创建数据目录: {data_dir}")
    
    # 检查设置文件
    settings_file = Path("settings.xml")
    if not settings_file.exists():
        # 创建默认设置文件
        default_settings = f'''<?xml version="1.0" encoding="UTF-8"?>
<settings>
    <save_path>{data_dir}</save_path>
    <auto_save>true</auto_save>
    <theme>light</theme>
    <startup_mode>auto</startup_mode>
</settings>'''
        
        with open(settings_file, "w", encoding="utf-8") as f:
            f.write(default_settings)
        print("✅ 已创建默认设置文件")
    
    return True


def smart_launcher():
    """智能启动器 - 自动选择最佳运行方式"""
    print("🚀 智能启动器 - 自动选择最佳运行方式...")
    
    # 尝试GUI模式
    gui_available = False
    try:
        import tkinter
        gui_available = True
        print("✅ GUI模式可用")
    except ImportError:
        print("❌ GUI模式不可用")
    
    # Web模式始终可用
    print("✅ Web模式可用")
    
    # 根据环境自动选择
    if gui_available and not sys.argv[1:]:  # 没有命令行参数时优先GUI
        print("🖥️  启动GUI模式...")
        return start_gui_mode()
    else:
        print("🌐 启动Web模式...")
        return start_web_mode()


def start_gui_mode():
    """启动GUI模式"""
    try:
        # 检查GUI文件是否存在
        if not Path("daily_planner.py").exists():
            print("❌ daily_planner.py 文件不存在")
            print("🔄 切换到Web模式...")
            return start_web_mode()
        
        import daily_planner
        daily_planner.main()
        return True
    except Exception as e:
        print(f"❌ GUI模式启动失败: {e}")
        print("🔄 自动切换到Web模式...")
        return start_web_mode()


def start_web_mode():
    """启动Web模式"""
    try:
        # 检查Web文件是否存在
        required_files = ["web_server.py", "index.html", "style.css", "script.js"]
        missing_files = [f for f in required_files if not Path(f).exists()]
        
        if missing_files:
            print(f"❌ 缺少文件: {', '.join(missing_files)}")
            return False
        
        print("🌐 启动Web服务器...")
        import web_server
        
        # 在后台启动服务器
        import threading
        server_thread = threading.Thread(target=web_server.main, daemon=True)
        server_thread.start()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 自动打开浏览器
        print("🔗 正在打开浏览器...")
        webbrowser.open("http://localhost:8000")
        
        print("✅ Web模式已启动")
        print("💡 在浏览器中使用应用程序")
        print("💡 按 Ctrl+C 退出")
        
        try:
            # 保持程序运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 再见!")
            return True
            
    except Exception as e:
        print(f"❌ Web模式启动失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("📅 QuirkLog 每日计划与总结应用程序")
    print("=" * 50)
    print(f"🖥️  平台: {platform.system()} {platform.machine()}")
    
    try:
        # 1. 检查Python版本
        if not check_python_version():
            input("按回车键退出...")
            return
        
        print()
        
        # 2. 检查和安装依赖
        install_missing_modules()
        
        print()
        
        # 3. 自动配置环境
        auto_setup_environment()
        
        print()
        
        # 4. 智能启动
        success = smart_launcher()
        
        if not success:
            print("\n❌ 应用程序启动失败")
            print("💡 请检查错误信息并重试")
            input("按回车键退出...")
        
    except KeyboardInterrupt:
        print("\n❌ 用户取消启动")
    except Exception as e:
        print(f"\n❌ 启动过程出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")


if __name__ == "__main__":
    main()
