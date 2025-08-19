#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 每日计划与总结应用程序启动器
Web版本专用启动器
"""

import sys
from datetime import datetime


def run_web_version():
    """运行Web版本"""
    print("🌐 启动Web版本...")
    try:
        import web_server
        web_server.main()
    except Exception as e:
        print(f"❌ Web版本启动失败: {e}")
        return False
    return True


def start_weekly_task_background():
    """在后台启动定时任务"""
    try:
        import weekly_task
        task_manager = weekly_task.WeeklyTaskManager()
        task_manager.start()
        print("✅ 定时任务已在后台启动")
    except Exception as e:
        print(f"⚠️ 定时任务启动失败: {e}")


def main():
    """主函数"""
    today = datetime.now().strftime("%Y年%m月%d日")
    print(f"🌞 {today} QuirkLog 每日计划与总结应用程序")
    print("=" * 50)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--web" or sys.argv[1] == "-w":
            if run_web_version():
                # 启动后在后台运行定时任务
                start_weekly_task_background()
            return
        elif sys.argv[1] == "--task" or sys.argv[1] == "-t":
            print("⏰ 启动定时任务管理器...")
            try:
                import weekly_task
                weekly_task.main()
            except Exception as e:
                print(f"❌ 定时任务启动失败: {e}")
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("\n使用说明:")
            print("  python launcher.py         # 启动Web版本")
            print("  python launcher.py --web   # 启动Web版本")
            print("  python launcher.py --task  # 启动定时任务管理器")
            print("  python launcher.py --help  # 显示帮助信息")
            print("\n功能说明:")
            print("  - Web版本: 现代化浏览器界面，支持计划管理和总结功能")
            print("  - 定时任务: AI每周洞察自动生成，需要配置OpenRouter API")
            return
    
    # 默认启动Web版本
    print("🚀 正在启动应用程序...")
    if run_web_version():
        # 在后台启动定时任务
        start_weekly_task_background()


if __name__ == "__main__":
    main()
