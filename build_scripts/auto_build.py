#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 自动构建和分发脚本
一键生成跨平台可执行文件包
"""

import os
import sys
import subprocess
import platform
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# 确保工作目录在项目根目录
script_dir = Path(__file__).parent
project_root = script_dir.parent
os.chdir(project_root)

APP_NAME = "QuirkLog"
APP_VERSION = "1.0.0"

def install_build_dependencies():
    """安装构建依赖"""
    print("📦 安装构建依赖...")
    
    # 安装 PyInstaller
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "pyinstaller==5.13.2", "Pillow==10.0.0"
        ], check=True)
        print("✅ 构建依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 构建依赖安装失败")
        return False

def create_simple_spec_file():
    """创建简化的 PyInstaller 规格文件"""
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

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
        'webbrowser', 'http.server', 'socketserver', 'threading',
        'json', 'xml.etree.ElementTree', 'datetime', 'pathlib',
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
)
"""
    
    with open(f"{APP_NAME}.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ 规格文件已创建")

def build_with_pyinstaller():
    """使用 PyInstaller 构建"""
    print("🔨 开始构建可执行文件...")
    
    try:
        # 创建规格文件
        create_simple_spec_file()
        
        # 运行 PyInstaller
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean", "--noconfirm", f"{APP_NAME}.spec"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ 构建成功!")
            return True
        else:
            print(f"❌ 构建失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 构建超时")
        return False
    except Exception as e:
        print(f"❌ 构建过程出错: {e}")
        return False

def create_installer_scripts():
    """创建各平台安装脚本"""
    system = platform.system()
    
    # Windows 安装脚本
    windows_script = f"""@echo off
chcp 65001 >nul
echo 🪟 QuirkLog 安装程序
echo ==================

echo 📦 正在安装 QuirkLog...

REM 创建程序目录
set "INSTALL_DIR=%USERPROFILE%\\QuirkLog"
if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%"

REM 复制文件
copy "{APP_NAME}.exe" "%INSTALL_DIR%\\"
if exist "*.html" copy "*.html" "%INSTALL_DIR%\\"
if exist "*.css" copy "*.css" "%INSTALL_DIR%\\"
if exist "*.js" copy "*.js" "%INSTALL_DIR%\\"
if exist "*.xml" copy "*.xml" "%INSTALL_DIR%\\"

REM 创建桌面快捷方式
set "DESKTOP=%USERPROFILE%\\Desktop"
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\\QuirkLog.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\{APP_NAME}.exe" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo ✅ 安装完成！桌面已创建快捷方式
pause
"""
    
    # Mac/Linux 安装脚本
    unix_script = f"""#!/bin/bash
echo "🍎 QuirkLog 安装程序"
echo "=================="

echo "📦 正在安装 QuirkLog..."

# 创建程序目录
INSTALL_DIR="$HOME/QuirkLog"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi
mkdir -p "$INSTALL_DIR"

# 复制文件
cp {APP_NAME} "$INSTALL_DIR/"
cp *.html "$INSTALL_DIR/" 2>/dev/null || true
cp *.css "$INSTALL_DIR/" 2>/dev/null || true
cp *.js "$INSTALL_DIR/" 2>/dev/null || true
cp *.xml "$INSTALL_DIR/" 2>/dev/null || true

# 设置执行权限
chmod +x "$INSTALL_DIR/{APP_NAME}"

# 创建启动脚本
echo '#!/bin/bash' > "$HOME/Desktop/QuirkLog.command"
echo "cd '$INSTALL_DIR'" >> "$HOME/Desktop/QuirkLog.command"
echo "./{APP_NAME}" >> "$HOME/Desktop/QuirkLog.command"
chmod +x "$HOME/Desktop/QuirkLog.command"

echo "✅ 安装完成！桌面已创建启动脚本"
"""
    
    # 写入文件
    with open("install_windows.bat", "w", encoding="utf-8") as f:
        f.write(windows_script)
    
    with open("install_unix.sh", "w") as f:
        f.write(unix_script)
    
    # 设置 Unix 脚本执行权限
    if os.name != 'nt':
        os.chmod("install_unix.sh", 0o755)
    
    print("✅ 安装脚本已创建")

def create_distribution_package():
    """创建分发包"""
    print("📦 创建分发包...")
    
    system = platform.system().lower()
    arch = platform.machine().lower()
    timestamp = datetime.now().strftime("%Y%m%d")
    
    # 包名
    package_name = f"{APP_NAME}-v{APP_VERSION}-{system}-{arch}-{timestamp}"
    
    # 创建临时目录
    temp_dir = Path("package_temp")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 复制可执行文件
        exe_name = f"{APP_NAME}.exe" if system == "windows" else APP_NAME
        dist_exe = Path("dist") / exe_name
        
        if dist_exe.exists():
            shutil.copy2(dist_exe, temp_dir / exe_name)
        else:
            print("❌ 找不到可执行文件")
            return False
        
        # 复制资源文件
        resource_files = ["index.html", "style.css", "script.js", "settings.xml", "README.md"]
        for file in resource_files:
            if Path(file).exists():
                shutil.copy2(file, temp_dir / file)
        
        # 复制安装脚本
        if system == "windows":
            shutil.copy2("install_windows.bat", temp_dir / "install.bat")
        else:
            shutil.copy2("install_unix.sh", temp_dir / "install.sh")
        
        # 创建说明文件
        readme_content = f"""# {APP_NAME} v{APP_VERSION}

## 安装说明

### Windows
1. 双击运行 install.bat
2. 按提示完成安装
3. 双击桌面上的 QuirkLog 快捷方式启动

### Mac/Linux
1. 在终端中运行: chmod +x install.sh && ./install.sh
2. 双击桌面上的 QuirkLog.command 启动

## 使用说明
- 支持Web和GUI两种界面模式
- 首次启动会自动选择最适合的模式
- 数据保存在用户目录的daylog文件夹中

构建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
构建平台: {platform.system()} {platform.machine()}
"""
        
        with open(temp_dir / "README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # 创建ZIP包
        zip_path = f"{package_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ 分发包已创建: {zip_path}")
        return True
        
    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def cleanup_build_files():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    files_to_remove = [
        f"{APP_NAME}.spec",
        "install_windows.bat",
        "install_unix.sh"
    ]
    
    dirs_to_remove = [
        "build",
        "__pycache__",
        "package_temp"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    print("✅ 清理完成")

def main():
    """主函数"""
    print(f"🚀 {APP_NAME} 自动打包工具")
    print("=" * 40)
    print(f"平台: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    try:
        # 1. 安装依赖
        if not install_build_dependencies():
            return
        
        print()
        
        # 2. 构建可执行文件
        if not build_with_pyinstaller():
            return
        
        print()
        
        # 3. 创建安装脚本
        create_installer_scripts()
        
        print()
        
        # 4. 创建分发包
        if not create_distribution_package():
            return
        
        print()
        
        # 5. 清理
        cleanup_build_files()
        
        print("\n🎉 打包完成！")
        print("\n📁 生成的文件:")
        for file in Path(".").glob(f"{APP_NAME}-v{APP_VERSION}-*.zip"):
            print(f"  📦 {file.name}")
        
        print("\n💡 使用说明:")
        print("1. 将ZIP文件发送给用户")
        print("2. 用户解压后运行install脚本即可安装")
        print("3. 安装完成后桌面会有启动图标")
        
    except KeyboardInterrupt:
        print("\n❌ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 打包失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
