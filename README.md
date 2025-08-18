# QuirkLog - 每日计划与总结应用程序

一个现代化的每日计划与总结应用程序，支持多平台运行，帮助您更好地管理时间、记录生活、进行自我反思和提升个人效率。

## 项目概述

QuirkLog 是一个全功能的个人时间管理和生活记录工具，采用Web优先的设计理念，兼容桌面GUI模式，支持跨平台部署。应用程序提供直观的界面，丰富的功能模块，以及完善的数据管理系统。

## 核心功能特性

### 📅 计划管理
- **智能计划添加**: 支持事件描述、重要等级、紧急程度分类
- **时间规划**: 开始时间设定和计划时长管理
- **状态跟踪**: 实时标记计划完成状态
- **优先级管理**: 基于艾森豪威尔矩阵的重要紧急度分类
- **批量操作**: 支持计划的批量编辑和删除

### 📝 反思总结
- **完成情况分析**: 自动统计计划完成率，生成可视化图表
- **个人成长记录**: 记录每日进步点和改进建议
- **感恩日记**: 记录感动和感恩的瞬间
- **每日思考**: 支持Markdown格式的深度思考记录
- **未完成原因分析**: 帮助识别时间管理中的问题

### 🌐 多模式界面
- **Web版本**: 现代化浏览器界面，响应式设计，跨平台兼容
- **GUI版本**: 原生桌面应用，tkinter界面，系统集成度高
- **智能启动器**: 自动检测环境，选择最佳运行模式

### 💾 数据管理系统
- **多格式保存**: JSON格式数据存储，易于备份和迁移
- **自动保存**: 智能自动保存机制，防止数据丢失
- **历史记录**: 按日期组织的历史记录浏览
- **数据导出**: 支持PDF导出，便于分享和打印
- **自定义路径**: 用户可自定义数据保存位置

### ⚙️ 个性化设置
- **文件命名**: 多种命名格式选择，支持自定义模式
- **保存路径**: 灵活的文件保存位置设定
- **界面主题**: 现代化UI设计，良好的用户体验
- **自动保存**: 可配置的自动保存功能

## 技术架构

### 前端技术
- **HTML5**: 语义化标记，响应式布局
- **CSS3**: 现代化样式设计，动画效果，Flexbox/Grid布局
- **JavaScript (ES6+)**: 面向对象编程，模块化设计，异步处理

### 后端技术
- **Python 3.x**: 核心开发语言
- **HTTP Server**: 基于Python标准库的轻量级Web服务器
- **tkinter**: 跨平台GUI框架

### 数据管理
- **JSON**: 轻量级数据存储格式
- **XML**: 配置文件管理
- **文件系统**: 本地数据持久化

### 构建和部署
- **PyInstaller**: 打包为独立可执行文件
- **跨平台支持**: Windows、macOS、Linux
- **自动化构建**: 一键打包脚本

## 系统要求

### 运行环境
- **Python**: 3.6 或更高版本
- **内存**: 最少 512MB RAM
- **存储**: 最少 100MB 可用空间
- **网络**: 本地运行，无需网络连接

### 操作系统支持
- **Windows**: Windows 10 或更高版本
- **macOS**: macOS 10.14 或更高版本  
- **Linux**: 主流发行版（Ubuntu 18.04+, CentOS 7+等）

## 快速开始

### 方式一：运行源代码（推荐开发者）
```bash
# 1. 克隆项目
git clone https://github.com/CattleZ/QuirkLog.git
cd QuirkLog

# 2. 运行应用程序（自动检测最佳模式）
python launcher.py

# 3. 手动选择运行模式
python launcher.py --web    # Web版本
python launcher.py --gui    # GUI版本
```

### 方式二：使用预编译版本
```bash
# 1. 下载对应平台的发布包
# 2. 解压文件
unzip QuirkLog-v1.0.0-*-*.zip

# 3. 运行安装脚本
# Windows: install.bat
# Mac/Linux: ./install.sh

# 4. 启动应用程序
# 双击桌面快捷方式或可执行文件
```

### 方式三：一键自动构建
```bash
# 构建可执行文件（适用于分发）
python auto_build.py
```

## 详细安装说明

### 开发环境设置
```bash
# 1. 确保Python环境
python --version  # 需要 3.6+

# 2. 安装依赖（如果有额外需求）
pip install -r requirements.txt

# 3. 直接运行
python launcher.py
```

### 生产环境部署

```bash
# 1. 构建可执行文件
python auto_build.py

# 2. 生成的文件将包含：
# - QuirkLog 可执行文件
# - 安装脚本（install.bat / install.sh）
# - 所有必需的资源文件
# - 使用说明文档
```

## 使用指南

### 基本操作流程
1. **启动应用**: 运行启动器或可执行文件
2. **制定计划**: 在"今日计划"标签页添加任务
3. **执行跟踪**: 在计划列表中标记完成状态
4. **反思总结**: 在"今日总结反思"标签页记录感悟
5. **数据保存**: 使用保存功能将数据持久化存储

### 高级功能使用
- **历史记录**: 通过侧边栏浏览历史记录
- **设置定制**: 通过设置面板个性化配置
- **数据导出**: 支持PDF格式导出，便于分享
- **批量操作**: 支持多项计划的批量管理

## 项目结构

### 核心文件
```
QuirkLog/
├── launcher.py              # 智能启动器
├── web_server.py           # Web服务器
├── daily_planner.py        # GUI版本
├── index.html              # Web前端页面
├── style.css               # 样式文件
├── script.js               # 前端逻辑
├── settings.xml            # 配置文件
└── README.md               # 项目说明
```

### 构建脚本
```
├── auto_build.py           # 自动构建脚本
├── build_package.py        # 打包工具
├── package.py              # 简单打包脚本
└── smart_launcher.py       # 智能启动器
```

### 配置文件
```
├── requirements.txt        # 运行时依赖
├── requirements-build.txt  # 构建时依赖
└── QuirkLog.spec          # PyInstaller配置
```

## 数据管理

### 存储格式
- **计划数据**: JSON格式，包含计划详情、状态、时间信息
- **总结数据**: JSON格式，包含反思内容、感悟记录
- **设置数据**: XML格式，存储用户个性化配置

### 数据安全
- 本地存储，保护隐私安全
- 支持自定义备份路径
- 数据格式开放，易于迁移

### 备份建议
```bash
# 备份用户数据目录
cp -r /path/to/save/directory /path/to/backup/location

# 备份配置文件
cp settings.xml /path/to/backup/location
```

## 开发指南

### 开发环境搭建
```bash
# 1. 克隆项目
git clone https://github.com/CattleZ/QuirkLog.git
cd QuirkLog

# 2. 设置虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装开发依赖
pip install -r requirements-build.txt

# 4. 开始开发
python launcher.py --web
```

### 代码规范
- 遵循 PEP 8 Python 代码规范
- 使用中文注释和适当的变量命名
- 保持代码简洁易读
- 优先使用现代Web技术和标准库

### 贡献方式
1. Fork 项目仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 创建 Pull Request

## 版本说明

### 当前版本：v1.0.0
- ✅ 完整的计划管理功能
- ✅ 丰富的反思总结模块
- ✅ 现代化Web界面
- ✅ 跨平台GUI支持
- ✅ 自动化构建系统
- ✅ 多格式数据导出

### 开发计划
- [ ] 移动端适配和响应式优化
- [ ] 计划提醒和通知功能
- [ ] 数据统计和可视化图表
- [ ] 计划模板和快速录入
- [ ] 云端同步和多设备支持
- [ ] 插件系统和功能扩展
- [ ] 更多主题和界面个性化
- [ ] 团队协作和分享功能

## 技术特点

### 架构优势
- **渐进式增强**: Web优先，向下兼容
- **零依赖部署**: 基于Python标准库
- **模块化设计**: 清晰的功能分离
- **跨平台兼容**: 一次开发，多平台运行

### 性能特点
- **轻量级**: 占用资源少，启动速度快
- **响应式**: 流畅的用户交互体验
- **离线优先**: 本地数据，无需网络依赖
- **可扩展**: 易于添加新功能和模块

## 故障排除

### 常见问题
**Q: 启动失败，提示找不到模块**
```bash
# 确保使用正确的Python版本
python --version
# 检查当前目录是否正确
pwd
# 重新运行启动器
python launcher.py
```

**Q: GUI版本无法启动**
```bash
# 强制使用Web版本
python launcher.py --web
# 或直接启动Web服务器
python web_server.py
```

**Q: 数据保存失败**
- 检查保存路径是否存在且可写
- 确认磁盘空间充足
- 查看设置面板中的保存路径配置

### 技术支持
- **问题反馈**: 通过GitHub Issues报告问题
- **功能建议**: 通过Discussions讨论新功能
- **文档问题**: 通过Pull Request改进文档

## 许可证与致谢

### 开源许可
本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

### 技术致谢
- Python软件基金会提供的Python语言支持
- tkinter GUI工具包
- 现代Web标准技术栈
- PyInstaller打包工具

### 贡献者
感谢所有为项目贡献代码、文档和建议的开发者。

---

**QuirkLog** - 让每一天都有记录，让每一次反思都有价值 ✨
