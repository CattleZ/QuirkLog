#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日计划与总结应用程序启动器
自动检测环境并选择合适的版本运行
"""

import sys
import subprocess
import os

def check_tkinter_available():
    """检查tkinter是否可用"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def run_web_version():
    """运行Web版本"""
    print("🌐 启动Web版本...")
    try:
        import web_server
        web_server.main()
    except Exception as e:
        print(f"❌ Web版本启动失败: {e}")


def run_gui_version():
    """运行GUI版本"""
    print("🖥️ 启动GUI版本...")
    try:
        import daily_planner
        daily_planner.main()
    except Exception as e:
        print(f"❌ GUI版本启动失败: {e}")
        print("🔄 自动切换到Web版本...")
        run_web_version()


def main():
    from datetime import datetime
    today = datetime.now().strftime("%Y年%m月%d日")
    print(f"📅 {today} 计划与总结应用程序")
    print("=" * 40)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--gui" or sys.argv[1] == "-g":
            if check_tkinter_available():
                run_gui_version()
            else:
                print("❌ tkinter不可用，无法运行GUI版本")
                print("💡 提示: 使用 --web 参数运行Web版本")
            return
        elif sys.argv[1] == "--web" or sys.argv[1] == "-w":
            run_web_version()
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\n使用说明:")
            print("  python launcher.py        # 自动选择版本")
            print("  python launcher.py --web  # 运行Web版本 (推荐)")
            print("  python launcher.py --gui  # 强制运行GUI版本")
            print("  python launcher.py --help # 显示帮助信息")
            return
    
    # 自动选择版本
    print("✅ 检测到多个版本可用")
    choice = input("\n选择运行版本:\n1. Web版本 (推荐)\n2. GUI版本\n请选择 (1-2) [默认1]: ").strip() or "1"
    
    if choice == "1":
        run_web_version()
    elif choice == "2":
        if check_tkinter_available():
            run_gui_version()
        else:
            print("❌ tkinter不可用，自动切换到Web版本")
            run_web_version()
    else:
        print("❌ 无效选择，使用默认Web版本")
        run_web_version()

if __name__ == "__main__":
    main()
