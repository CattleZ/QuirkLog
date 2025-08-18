# 构建与部署脚本目录

本目录包含QuirkLog项目的所有构建、打包和部署相关的脚本，用于将项目打包成可执行文件或发布包。

## 📋 脚本说明

| 脚本名称 | 功能 | 用途 | 推荐使用 |
|----------|------|------|----------|
| `auto_build.py` | 自动构建脚本 | 一键构建可执行文件，包含完整的打包流程 | ⭐⭐⭐ |
| `build_package.py` | 高级打包工具 | 提供更多自定义选项的打包功能 | ⭐⭐ |
| `package.py` | 简单打包脚本 | 基础的PyInstaller打包功能 | ⭐ |
| `smart_launcher.py` | 智能启动器 | 自动检测环境并选择最佳运行模式 | ⭐⭐⭐ |

## 🚀 使用方法

### 快速构建（推荐）

```bash
# 从项目根目录运行
cd QuirkLog

# 一键自动构建
python build_scripts/auto_build.py

# 构建完成后，可执行文件将生成在dist/目录中
```

### 高级构建选项

```bash
# 使用高级打包工具
python build_scripts/build_package.py

# 自定义打包选项
python build_scripts/build_package.py --options

# 简单打包（基础功能）
python build_scripts/package.py
```

### 智能启动器

```bash
# 智能启动器会自动检测最佳运行模式
python build_scripts/smart_launcher.py

# 也可以直接从项目根目录使用
python launcher.py  # 这会调用智能启动逻辑
```

## 🔧 构建配置

### 构建要求
- Python 3.6+ 环境
- 安装构建依赖：`pip install -r requirements-build.txt`
- 确保所有运行时依赖已安装：`pip install -r requirements.txt`

### 构建依赖
```bash
# 安装构建工具
pip install pyinstaller
pip install setuptools
pip install wheel

# 或者一次性安装
pip install -r requirements-build.txt
```

### 输出文件
构建完成后，将在以下位置生成文件：

```
dist/                       # 构建输出目录
├── QuirkLog/              # 可执行文件目录
│   ├── QuirkLog           # 主可执行文件 (Linux/Mac)
│   ├── QuirkLog.exe       # 主可执行文件 (Windows)
│   └── _internal/         # 依赖文件
├── QuirkLog.spec          # PyInstaller配置文件
└── build/                 # 临时构建文件
```

## 📦 构建脚本详解

### auto_build.py - 自动构建脚本
**功能特性：**
- 🔄 自动检测操作系统和Python环境
- 📦 一键构建包含所有依赖的可执行文件
- ✅ 自动验证构建结果
- 🛠 支持多平台构建（Windows、macOS、Linux）
- 📋 生成详细的构建报告

**使用场景：**
- 准备发布版本
- 快速构建测试版本
- 自动化CI/CD流程

### build_package.py - 高级打包工具
**功能特性：**
- ⚙️ 提供丰富的自定义选项
- 🎯 支持不同的打包模式
- 📊 详细的构建进度显示
- 🔧 可配置的资源包含/排除规则

**使用场景：**
- 需要特定构建配置
- 自定义资源文件处理
- 开发阶段的测试构建

### package.py - 简单打包脚本
**功能特性：**
- 📝 简洁的PyInstaller封装
- 🚀 快速构建基本可执行文件
- 💡 适合初学者使用

**使用场景：**
- 快速原型验证
- 学习构建流程
- 简单的测试构建

### smart_launcher.py - 智能启动器
**功能特性：**
- 🧠 智能环境检测
- 🔄 自动选择最佳运行模式
- 🌐 Web/GUI模式智能切换
- ⚡ 优化的启动流程

**使用场景：**
- 最终用户体验
- 跨平台部署
- 自动化启动脚本

## 🛠 自定义构建

### 修改构建配置
1. 编辑 `auto_build.py` 中的配置参数
2. 修改 `QuirkLog.spec` 文件（如果存在）
3. 更新 `requirements-build.txt` 添加新的构建依赖

### 添加资源文件
```python
# 在构建脚本中添加资源文件
datas = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('config', 'config'),
]
```

### 优化构建大小
```bash
# 使用UPX压缩（需要单独安装UPX）
python build_scripts/auto_build.py --compress

# 排除不必要的模块
python build_scripts/auto_build.py --exclude-modules
```

## 🐛 构建故障排除

### 常见问题

**Q: 构建失败，提示缺少模块**
```bash
# 确保安装了所有依赖
pip install -r requirements.txt
pip install -r requirements-build.txt

# 检查Python环境
python --version
pip list | grep pyinstaller
```

**Q: 可执行文件启动失败**
```bash
# 检查构建日志
cat build.log

# 在构建目录中手动测试
cd dist/QuirkLog
./QuirkLog  # Linux/Mac
# 或 QuirkLog.exe  # Windows
```

**Q: 构建文件过大**
```bash
# 使用--onefile选项构建单文件版本
python build_scripts/auto_build.py --onefile

# 或者排除不必要的依赖
python build_scripts/auto_build.py --minimal
```

**Q: 跨平台构建问题**
- 在目标平台上进行构建
- 使用Docker进行隔离构建
- 检查平台特定的依赖

### 调试模式
```bash
# 启用详细输出
python build_scripts/auto_build.py --verbose

# 保留临时文件用于调试
python build_scripts/auto_build.py --debug

# 测试构建但不清理
python build_scripts/auto_build.py --no-clean
```

## 📊 性能优化

### 构建速度优化
- 使用SSD存储进行构建
- 增加内存分配给构建进程
- 使用多核并行构建选项

### 文件大小优化
- 移除未使用的依赖
- 使用压缩选项
- 优化资源文件

### 启动速度优化
- 使用--onefile选项
- 预编译Python模块
- 优化导入顺序

## 📞 技术支持

### 获取帮助
```bash
# 查看构建脚本帮助
python build_scripts/auto_build.py --help
python build_scripts/build_package.py --help

# 检查构建环境
python -c "
import sys
import platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.system()} {platform.release()}')
try:
    import PyInstaller
    print(f'PyInstaller: {PyInstaller.__version__}')
except ImportError:
    print('PyInstaller: 未安装')
"
```

### 报告问题
- 提供完整的构建日志
- 说明操作系统和Python版本
- 描述具体的错误现象
- 提供复现步骤

---

*这些构建脚本帮助您轻松将QuirkLog打包成可执行文件，支持跨平台分发！* 🚀
