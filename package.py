#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 一键打包脚本
支持Mac和Windows平台
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def main():
    print("🚀 QuirkLog 一键打包工具")
    print("=" * 30)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        return
    
    print(f"✅ Python {sys.version.split()[0]}")
    print(f"✅ 平台: {platform.system()} {platform.machine()}")
    
    try:
        # 安装PyInstaller
        print("\n📦 安装 PyInstaller...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "pyinstaller==5.13.2"
        ], check=True)
        
        # 构建可执行文件
        print("\n🔨 构建可执行文件...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name=QuirkLog",
            "--add-data=index.html:.",
            "--add-data=style.css:.",
            "--add-data=script.js:.",
            "--add-data=settings.xml:.",
            "--clean",
            "--noconfirm",
            "launcher.py"
        ]
        
        # Windows需要不同的分隔符
        if platform.system() == "Windows":
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--name=QuirkLog",
                "--add-data=index.html;.",
                "--add-data=style.css;.",
                "--add-data=script.js;.",
                "--add-data=settings.xml;.",
                "--clean",
                "--noconfirm",
                "launcher.py"
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 构建成功!")
            
            # 检查生成的文件
            exe_name = "QuirkLog.exe" if platform.system() == "Windows" else "QuirkLog"
            exe_path = Path("dist") / exe_name
            
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"📁 可执行文件: {exe_path} ({size_mb:.1f} MB)")
                
                # 创建简单的安装说明
                readme = f"""# QuirkLog 每日计划应用程序

## 安装说明

### 快速开始
1. 将 {exe_name} 复制到任意文件夹
2. 双击运行 {exe_name}
3. 首次运行会自动在浏览器中打开Web界面

### 使用说明
- 应用程序会自动选择最佳运行模式
- Web模式: 在浏览器中使用,跨平台兼容性最佳
- GUI模式: 原生桌面界面(如果系统支持)

### 数据存储
应用程序会在用户目录下创建 daylog 文件夹存储数据

### 系统要求
- Windows 10+, macOS 10.14+, 或 Linux
- 最少 512MB 内存
- 最少 100MB 存储空间

版本: 1.0.0
构建时间: {platform.system()} {platform.machine()}
"""
                
                with open("dist/README.txt", "w", encoding="utf-8") as f:
                    f.write(readme)
                
                print("📝 已创建 README.txt 使用说明")
                print("\n🎉 打包完成!")
                print(f"\n📂 文件位置: {exe_path.absolute()}")
                print("💡 可以直接分发 dist 文件夹中的文件")
                
            else:
                print("❌ 找不到生成的可执行文件")
        else:
            print(f"❌ 构建失败: {result.stderr}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
    except Exception as e:
        print(f"❌ 打包过程出错: {e}")
    
    # 询问是否清理临时文件
    try:
        choice = input("\n🧹 是否清理临时文件? (y/n) [y]: ").strip().lower()
        if choice in ('', 'y', 'yes'):
            if os.path.exists("build"):
                shutil.rmtree("build")
                print("✅ 已清理 build 目录")
            if os.path.exists("QuirkLog.spec"):
                os.remove("QuirkLog.spec")
                print("✅ 已清理 spec 文件")
    except KeyboardInterrupt:
        print("\n👋 再见!")

if __name__ == "__main__":
    main()
