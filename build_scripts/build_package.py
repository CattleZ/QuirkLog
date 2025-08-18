#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 每日计划应用程序打包脚本
支持 Mac 和 Windows 平台的可执行文件生成
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# 确保工作目录在项目根目录
script_dir = Path(__file__).parent
project_root = script_dir.parent
os.chdir(project_root)

# 应用信息
APP_NAME = "QuirkLog"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "每日计划与总结应用程序"
APP_AUTHOR = "QuirkLog Team"

# 打包配置
PYINSTALLER_SPEC = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('index.html', '.'),
        ('style.css', '.'),
        ('script.js', '.'),
        ('settings.xml', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'webbrowser',
        'http.server',
        'socketserver',
        'threading',
        'json',
        'xml.etree.ElementTree',
        'datetime',
        'pathlib',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if platform.system() == 'Windows' else 'icon.icns',
)

# Mac 应用程序包
{'app = BUNDLE(exe, name="' + APP_NAME + '.app", icon="icon.icns", bundle_identifier="com.quirklog.dailyplanner")' if platform.system() == 'Darwin' else ''}
"""

def check_dependencies():
    """检查打包依赖是否已安装"""
    print("🔍 检查打包依赖...")
    
    required_packages = ['pyinstaller', 'Pillow']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print("\n📦 安装缺失的依赖...")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
    
    return len(missing_packages) == 0

def create_icons():
    """创建应用程序图标"""
    print("🎨 创建应用程序图标...")
    
    # 创建简单的图标文件（实际项目中应该使用专业设计的图标）
    icon_dir = Path("icons")
    icon_dir.mkdir(exist_ok=True)
    
    # 这里只是创建占位图标文件
    # 在实际使用中，你需要准备真正的 .ico 和 .icns 图标文件
    with open("icon.ico", "w") as f:
        f.write("# Placeholder for Windows icon")
    
    with open("icon.icns", "w") as f:
        f.write("# Placeholder for Mac icon")

def build_executable():
    """构建可执行文件"""
    print(f"🔨 开始构建 {platform.system()} 平台的可执行文件...")
    
    # 创建 PyInstaller 规格文件
    spec_content = PYINSTALLER_SPEC.strip()
    with open(f"{APP_NAME}.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    # 运行 PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        f"{APP_NAME}.spec"
    ]
    
    print(f"📝 执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 构建成功!")
        return True
    else:
        print(f"❌ 构建失败: {result.stderr}")
        return False

def create_installer_script():
    """创建安装脚本"""
    system = platform.system()
    
    if system == "Darwin":  # Mac
        create_mac_installer()
    elif system == "Windows":
        create_windows_installer()
    else:
        create_linux_installer()

def create_mac_installer():
    """创建 Mac 安装脚本"""
    installer_content = f'''#!/bin/bash
# QuirkLog Mac 安装脚本

echo "🍎 QuirkLog Mac 安装程序"
echo "=========================="

# 检查是否为 Mac 系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此安装程序仅适用于 macOS 系统"
    exit 1
fi

# 创建应用程序目录
APP_DIR="/Applications/{APP_NAME}.app"
if [ -d "$APP_DIR" ]; then
    echo "🗑️  删除旧版本..."
    rm -rf "$APP_DIR"
fi

# 复制应用程序
echo "📦 安装 {APP_NAME}..."
cp -R "dist/{APP_NAME}.app" "/Applications/"

# 设置权限
chmod +x "/Applications/{APP_NAME}.app/Contents/MacOS/{APP_NAME}"

echo "✅ 安装完成！"
echo "💡 你可以在启动台或应用程序文件夹中找到 {APP_NAME}"

# 询问是否立即启动
read -p "🚀 是否立即启动 {APP_NAME}? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "/Applications/{APP_NAME}.app"
fi
'''
    
    with open("install_mac.sh", "w") as f:
        f.write(installer_content)
    
    # 设置执行权限
    os.chmod("install_mac.sh", 0o755)
    print("✅ Mac 安装脚本已创建: install_mac.sh")

def create_windows_installer():
    """创建 Windows 安装脚本"""
    installer_content = f'''@echo off
chcp 65001 >nul
echo 🪟 QuirkLog Windows 安装程序
echo ==============================

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ 检测到管理员权限
) else (
    echo ⚠️  建议以管理员身份运行此安装程序
)

REM 创建程序目录
set "INSTALL_DIR=%ProgramFiles%\\{APP_NAME}"
if exist "%INSTALL_DIR%" (
    echo 🗑️  删除旧版本...
    rmdir /s /q "%INSTALL_DIR%"
)

echo 📦 安装 {APP_NAME}...
mkdir "%INSTALL_DIR%"
xcopy /E /I /H /Y "dist\\{APP_NAME}.exe" "%INSTALL_DIR%\\"

REM 创建桌面快捷方式
set "DESKTOP=%USERPROFILE%\\Desktop"
echo 🔗 创建桌面快捷方式...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\\{APP_NAME}.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{APP_NAME}.exe'; $Shortcut.Save()"

REM 创建开始菜单快捷方式
set "STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\\{APP_NAME}.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{APP_NAME}.exe'; $Shortcut.Save()"

echo ✅ 安装完成！
echo 💡 你可以在桌面或开始菜单中找到 {APP_NAME}

REM 询问是否立即启动
set /p "choice=🚀 是否立即启动 {APP_NAME}? (y/n): "
if /i "%choice%"=="y" (
    start "" "%INSTALL_DIR%\\{APP_NAME}.exe"
)

pause
'''
    
    with open("install_windows.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✅ Windows 安装脚本已创建: install_windows.bat")

def create_linux_installer():
    """创建 Linux 安装脚本"""
    installer_content = f'''#!/bin/bash
# QuirkLog Linux 安装脚本

echo "🐧 QuirkLog Linux 安装程序"
echo "=========================="

# 检查是否为 Linux 系统
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ 此安装程序仅适用于 Linux 系统"
    exit 1
fi

# 创建应用程序目录
INSTALL_DIR="/opt/{APP_NAME}"
if [ -d "$INSTALL_DIR" ]; then
    echo "🗑️  删除旧版本..."
    sudo rm -rf "$INSTALL_DIR"
fi

# 复制应用程序
echo "📦 安装 {APP_NAME}..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -R dist/{APP_NAME}/* "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/{APP_NAME}"

# 创建符号链接
sudo ln -sf "$INSTALL_DIR/{APP_NAME}" "/usr/local/bin/{APP_NAME.lower()}"

# 创建桌面图标
DESKTOP_FILE="[Desktop Entry]
Version=1.0
Type=Application
Name={APP_NAME}
Comment={APP_DESCRIPTION}
Exec=$INSTALL_DIR/{APP_NAME}
Icon=$INSTALL_DIR/icon.png
Terminal=false
StartupNotify=true
Categories=Office;Productivity;"

echo "$DESKTOP_FILE" | sudo tee "/usr/share/applications/{APP_NAME.lower()}.desktop" > /dev/null
sudo chmod 644 "/usr/share/applications/{APP_NAME.lower()}.desktop"

echo "✅ 安装完成！"
echo "💡 你可以在应用程序菜单中找到 {APP_NAME}"
echo "💡 或者在终端中输入 '{APP_NAME.lower()}' 启动"

# 询问是否立即启动
read -p "🚀 是否立即启动 {APP_NAME}? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$INSTALL_DIR/{APP_NAME}" &
fi
'''
    
    with open("install_linux.sh", "w") as f:
        f.write(installer_content)
    
    # 设置执行权限
    os.chmod("install_linux.sh", 0o755)
    print("✅ Linux 安装脚本已创建: install_linux.sh")

def create_package_info():
    """创建包信息文件"""
    package_info = f"""# {APP_NAME} 可执行文件包

## 应用信息
- **名称**: {APP_NAME}
- **版本**: {APP_VERSION}
- **描述**: {APP_DESCRIPTION}
- **作者**: {APP_AUTHOR}
- **平台**: {platform.system()} {platform.machine()}

## 系统要求
- 操作系统: Windows 10+, macOS 10.14+, 或 Linux (Ubuntu 18.04+)
- 内存: 最少 512MB RAM
- 存储空间: 最少 100MB 可用空间

## 安装说明

### Windows
1. 下载 `{APP_NAME}-windows.zip`
2. 解压到任意目录
3. 以管理员身份运行 `install_windows.bat`

### Mac
1. 下载 `{APP_NAME}-mac.zip`
2. 解压到任意目录
3. 在终端中运行 `chmod +x install_mac.sh && ./install_mac.sh`

### Linux
1. 下载 `{APP_NAME}-linux.zip`
2. 解压到任意目录
3. 在终端中运行 `chmod +x install_linux.sh && ./install_linux.sh`

## 使用说明
应用程序提供两种运行模式：
1. **Web模式**: 在浏览器中运行，跨平台兼容性最佳
2. **GUI模式**: 原生桌面应用程序界面

首次启动时，应用程序会自动选择最适合的运行模式。

## 数据存储
- 配置文件: `settings.xml`
- 计划数据: 存储在用户指定的目录中（默认为下载文件夹下的 daylog 目录）

## 技术支持
如有问题，请联系开发团队或查看项目文档。
"""
    
    with open("PACKAGE_README.md", "w", encoding="utf-8") as f:
        f.write(package_info)
    
    print("✅ 包信息文件已创建: PACKAGE_README.md")

def cleanup():
    """清理临时文件"""
    print("🧹 清理临时文件...")
    
    files_to_remove = [
        f"{APP_NAME}.spec",
        "icon.ico",
        "icon.icns",
    ]
    
    dirs_to_remove = [
        "build",
        "__pycache__",
        "icons",
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"  🗑️  删除文件: {file}")
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  🗑️  删除目录: {dir_name}")

def main():
    """主函数"""
    print(f"🚀 {APP_NAME} 打包工具")
    print("=" * 50)
    print(f"平台: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    print()
    
    try:
        # 检查依赖
        if not check_dependencies():
            print("❌ 依赖检查失败")
            return
        
        # 创建图标
        create_icons()
        
        # 构建可执行文件
        if not build_executable():
            print("❌ 构建失败")
            return
        
        # 创建安装脚本
        create_installer_script()
        
        # 创建包信息
        create_package_info()
        
        print("\n🎉 打包完成！")
        print("\n📁 生成的文件:")
        print(f"  - dist/{APP_NAME}(.exe/.app) - 可执行文件")
        print(f"  - install_*.sh/bat - 安装脚本")
        print(f"  - PACKAGE_README.md - 使用说明")
        
        print("\n📦 打包分发建议:")
        print("1. 将 dist 目录和安装脚本一起压缩")
        print("2. 为每个平台创建单独的压缩包")
        print("3. 在 README 中包含安装和使用说明")
        
        # 询问是否清理临时文件
        choice = input("\n🧹 是否清理临时文件? (y/n) [y]: ").strip().lower()
        if choice in ('', 'y', 'yes'):
            cleanup()
        
    except KeyboardInterrupt:
        print("\n❌ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 打包过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
