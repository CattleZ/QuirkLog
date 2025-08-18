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

### 🤖 AI智能助手
- **每周洞察**: 集成OpenRouter AI，每周末自动生成个人成长建议
- **定时任务**: 可配置的定时任务系统，自动执行AI咨询
- **个性化建议**: 基于AI的每周总结和下周计划指导
- **智能反思**: AI生成的自我反思问题和成长建议
- **Web界面配置**: 通过Web界面直观配置AI功能，无需手动编辑文件
- **多模型支持**: 支持多种AI模型选择，包括免费和付费选项
- **安全可靠**: 本地存储API密钥，支持连接测试，有完善的错误处理

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

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置AI功能（可选）
# 方式A: 通过Web界面配置（推荐）
# 启动应用后，点击"⚙️ 设置" -> "AI智能助手设置"

# 方式B: 手动配置文件
cp config_template.py config.py
# 编辑config.py添加OpenRouter API密钥

# 4. 启动应用程序
python launcher.py          # 智能启动器（推荐）
python main_launcher.py     # 包含AI功能的启动器
python web_server.py        # 直接启动Web版本
python daily_planner.py     # 直接启动GUI版本

# 5. 构建可执行文件（可选）
python build_scripts/auto_build.py  # 一键构建发布版本
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
python build_scripts/auto_build.py
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
python build_scripts/auto_build.py

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

### 构建与分发
- **一键构建**: 使用 `python build_scripts/auto_build.py` 构建可执行文件
- **自定义打包**: 使用 `python build_scripts/build_package.py` 进行高级打包
- **跨平台支持**: 在目标平台上构建对应的可执行文件
- **构建说明**: 详细的构建指南请参考 [build_scripts/README.md](build_scripts/README.md)

## AI智能助手功能详解

### 🔧 AI功能配置

#### 1. 快速配置指南

**步骤1: 启动Web界面**
```bash
cd QuirkLog
python web_server.py
```

**步骤2: 获取API密钥**
1. 访问 https://openrouter.ai/
2. 注册免费账户
3. 在控制台创建API密钥（格式：`sk-or-v1-xxxxxxxxxxxxxxxx`）

**步骤3: 配置AI功能**
1. 在浏览器中打开 http://localhost:8000
2. 点击右上角 "⚙️ 设置" 按钮
3. 找到 "🤖 AI智能助手设置" 区域
4. 启用 "启用AI功能" 开关
5. 输入API密钥到 "OpenRouter API密钥" 字段
6. 选择合适的AI模型（可选）
7. 点击 "🧪 测试AI连接" 验证配置
8. 点击 "💾 保存设置" 完成配置

#### 2. 支持的AI模型

| 模型名称 | 类型 | 适用场景 |
|----------|------|----------|
| deepseek/deepseek-r1-0528-qwen3-8b:free | 免费 | 日常使用，中文友好（默认） |
| openai/gpt-3.5-turbo | 付费 | 高质量对话 |
| openai/gpt-4o-mini | 付费 | 更强推理能力 |
| anthropic/claude-3-haiku | 付费 | 长文本处理 |
| google/gemini-flash-1.5 | 付费 | 快速响应 |
| meta-llama/llama-3.1-8b-instruct:free | 免费 | 开源替代 |
| microsoft/wizardlm-2-8x22b | 付费 | 高级推理 |

#### 3. 配置文件说明

配置成功后，设置将保存在`settings.xml`文件中：

```xml
<ai>
    <enabled>true</enabled>
    <openrouterApiKey>sk-or-v1-your-api-key-here</openrouterApiKey>
    <openrouterBaseUrl>https://openrouter.ai/api/v1</openrouterBaseUrl>
    <openrouterModel>deepseek/deepseek-r1-0528-qwen3-8b:free</openrouterModel>
</ai>
```

### 🚀 AI功能使用

#### 1. 每周定时任务

配置完成后，AI功能会自动执行：
- **每周六上午9点**: 自动获取AI洞察
- **每周日晚上7点**: 获取周末反思

手动执行方式：
```bash
# 使用主启动器（推荐）
python main_launcher.py

# 直接运行每周任务
python weekly_task.py

# 测试AI功能
python test_weekly_task.py
```

#### 2. AI功能特性

- **🔄 自动执行**: 基于schedule库的定时任务系统
- **🤖 AI洞察**: 使用深度学习模型生成个性化建议
- **💾 数据保存**: AI生成的洞察自动保存到`weekly_insights/`目录
- **🧪 测试模式**: 支持立即执行任务进行测试
- **📊 个性化**: 基于用户的计划和总结数据生成建议

#### 3. 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端界面       │    │   后端API       │    │   配置存储       │
│   (HTML/CSS/JS) │────│   (Python)      │────│   (XML)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户交互       │    │   配置验证       │    │   持久化存储     │
│   - 设置开关     │    │   - API测试     │    │   - XML格式     │
│   - API密钥     │    │   - 数据校验     │    │   - 自动更新     │
│   - 模型选择     │    │   - 错误处理     │    │   - 安全存储     │
│   - 连接测试     │    │   - 智能重试     │    │   - 备份恢复     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🛠 故障排除

#### 常见问题解决

**Q: API连接测试失败**
- 检查API密钥是否正确复制
- 确认网络连接正常
- 验证OpenRouter账户是否有效
- 检查API密钥格式（应以`sk-or-v1-`开头）

**Q: 提示"未安装openai库"**
```bash
pip install openai schedule
```

**Q: 定时任务不执行**
- 确保AI功能已启用（设置中的开关）
- 检查API密钥配置是否正确
- 运行测试模式验证功能：`python test_weekly_task.py`
- 检查`settings.xml`文件是否存在且格式正确

**Q: 找不到设置文件**
- 设置会自动保存到项目根目录的`settings.xml`
- 如果文件丢失，重新通过Web界面配置即可
- 确保程序有写入权限

#### 调试命令

```bash
# 检查AI配置状态
python tests/test_ai_config.py

# 测试API连接
python -c "from weekly_task import WeeklyTaskManager; mgr = WeeklyTaskManager(); mgr.run_task_now()"

# 查看当前设置
cat settings.xml

# 手动测试模型配置
python tests/test_model_config.py

# 演示完整功能
python tests/demo_ai_config.py
```

### 🔒 安全与隐私

- **本地存储**: API密钥和设置仅保存在本地`settings.xml`文件中
- **安全传输**: 所有API请求使用HTTPS加密
- **数据隐私**: AI洞察仅保存在本地`weekly_insights/`目录中
- **可选功能**: 随时可以通过设置界面禁用AI功能
- **密钥保护**: 支持密钥显示/隐藏切换，防止意外泄露

### 📋 API使用说明

#### 免费额度
- OpenRouter提供每月免费额度
- 默认使用免费模型：`deepseek/deepseek-r1-0528-qwen3-8b:free`
- 建议合理使用，避免频繁测试
- 可在OpenRouter控制台查看使用情况

#### 配置优先级
1. **命令行参数**: 最高优先级
2. **XML配置文件**: 中等优先级
3. **环境变量**: 最低优先级
4. **默认值**: 兜底配置

#### 编程接口
```python
# 使用默认配置（从XML读取）
manager = WeeklyTaskManager()

# 指定特定模型
manager = WeeklyTaskManager(model="gpt-3.5-turbo")

# 获取当前配置
print(f"当前模型: {manager.model}")
print(f"API状态: {'已配置' if manager.client else '未配置'}")
```

## 项目结构

### 核心文件
```
QuirkLog/
├── launcher.py              # 智能启动器
├── main_launcher.py         # 包含AI功能的启动器
├── web_server.py           # Web服务器
├── daily_planner.py        # GUI版本
├── daily_planner_cli.py    # 命令行版本
├── weekly_task.py          # AI定时任务系统
├── index.html              # Web前端页面
├── style.css               # 样式文件
├── script.js               # 前端逻辑
├── settings.xml            # 配置文件
├── config_template.py      # 配置模板
└── README.md               # 项目说明
```

### AI功能相关文件
```
├── weekly_task.py          # AI定时任务核心模块
└── weekly_insights/        # AI生成的洞察保存目录
```

### 测试与演示脚本
```
tests/                      # 测试脚本目录
├── README.md              # 测试说明文档
├── test_ai_config.py      # AI配置测试脚本
├── test_weekly_task.py    # AI功能测试脚本
├── test_model_config.py   # AI模型配置测试
└── demo_ai_config.py      # AI功能演示脚本
```

### 构建与部署脚本
```
build_scripts/              # 构建脚本目录
├── README.md              # 构建脚本说明文档
├── auto_build.py          # 自动构建脚本（推荐）
├── build_package.py       # 高级打包工具
├── package.py             # 简单打包脚本
└── smart_launcher.py      # 智能启动器
```

### 文档与配置
```
├── requirements.txt        # 运行时依赖
├── requirements-build.txt  # 构建时依赖
├── QuirkLog.spec          # PyInstaller配置
├── run_tests.py           # 测试运行器
├── build_scripts/         # 构建脚本目录
├── docs/                  # 文档目录
│   └── archived/          # 归档文档
└── tests/                 # 测试脚本目录
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
pip install -r requirements.txt
pip install -r requirements-build.txt

# 4. 配置AI功能（开发测试）
# 方式A: 通过Web界面配置（推荐）
python web_server.py
# 打开 http://localhost:8000，点击"⚙️ 设置"进行配置

# 方式B: 手动配置文件
cp config_template.py config.py
# 编辑config.py添加测试API密钥

# 5. 开始开发
python launcher.py              # 基础版本
python main_launcher.py         # 包含AI功能
python tests/test_weekly_task.py  # 测试AI定时任务
```

### AI功能开发说明
本项目集成了OpenRouter AI API，提供每周智能洞察功能：

#### 核心特性
- **Web界面配置**: 用户可通过Web界面"⚙️ 设置"直观配置OpenRouter API密钥和模型选择
- **多模型支持**: 支持多种AI模型，包括免费的DeepSeek和付费的GPT、Claude等
- **定时任务**: 使用schedule库实现每周末自动执行AI洞察生成
- **安全存储**: API密钥和配置安全保存在本地`settings.xml`文件中
- **数据管理**: AI生成的洞察自动保存在`weekly_insights/`目录的JSON文件中

#### 技术实现
- **配置系统**: XML格式配置文件，支持运行时更新
- **API集成**: 基于OpenAI兼容的API接口，支持多种模型
- **错误处理**: 完善的异常处理和重试机制
- **测试支持**: 提供多个测试脚本验证功能正常性

#### 开发工具
```bash
# AI功能测试
python tests/test_ai_config.py        # 测试配置读取
python tests/test_weekly_task.py      # 测试定时任务
python tests/test_model_config.py     # 测试模型配置
python tests/demo_ai_config.py        # 功能演示

# 批量运行测试
for test in tests/test_*.py; do python "$test"; done

# Web界面开发
python web_server.py            # 启动开发服务器
# 修改 index.html, script.js, style.css 进行界面开发
```

### 项目架构
```
QuirkLog/
├── daily_planner.py      # GUI主程序
├── daily_planner_cli.py  # 命令行版本
├── web_server.py         # Web服务器
├── launcher.py           # 智能启动器
├── main_launcher.py      # 包含AI的启动器
├── weekly_task.py        # AI定时任务系统
├── config_template.py    # 配置模板
├── index.html            # Web界面
├── script.js             # 前端逻辑
├── style.css             # 样式文件
├── settings.xml          # 配置文件
├── requirements.txt      # 项目依赖
└── tests/                # 测试与演示脚本目录
    ├── test_ai_config.py     # AI配置测试
    ├── test_weekly_task.py   # AI功能测试
    ├── test_model_config.py  # 模型配置测试
    └── demo_ai_config.py     # AI功能演示
```

### 代码规范
- 遵循 PEP 8 Python 代码规范
- 使用中文注释和适当的变量命名
- 保持代码简洁易读
- 优先使用现代Web技术和标准库
- AI功能模块化设计，易于扩展

### 贡献方式
1. Fork 项目仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 创建 Pull Request

### 测试与质量保证

#### 测试脚本说明
项目包含完整的测试套件，位于`tests/`目录：

| 测试脚本 | 功能 | 用途 |
|----------|------|------|
| `test_ai_config.py` | AI配置测试 | 验证XML配置读取、API密钥设置等 |
| `test_weekly_task.py` | AI定时任务测试 | 测试定时任务机制和API连接 |
| `test_model_config.py` | AI模型配置测试 | 验证多模型支持和配置切换 |
| `demo_ai_config.py` | AI功能演示 | 完整的功能演示和交互体验 |

#### 运行测试
```bash
# 运行单个测试
python tests/test_ai_config.py

# 运行所有测试
for test in tests/test_*.py; do
    echo "执行测试: $test"
    python "$test"
    echo "---"
done

# 运行演示程序
python tests/demo_ai_config.py
```

#### 测试覆盖范围
- ✅ AI配置系统完整性测试
- ✅ OpenRouter API连接验证
- ✅ 多AI模型配置测试
- ✅ 定时任务调度验证
- ✅ 数据持久化测试
- ✅ 错误处理机制验证
- ✅ 配置优先级测试

#### 持续集成
- 代码提交前请运行完整测试套件
- 新功能开发请添加相应测试
- 所有测试通过后再提交Pull Request
- 详细测试说明请参考：[tests/README.md](tests/README.md)
- 构建脚本说明请参考：[build_scripts/README.md](build_scripts/README.md)

## 版本说明

### 当前版本：v1.0.0
- ✅ 完整的计划管理功能
- ✅ 丰富的反思总结模块
- ✅ 现代化Web界面
- ✅ 跨平台GUI支持
- ✅ 自动化构建系统
- ✅ 多格式数据导出
- ✅ AI智能助手功能
- ✅ Web界面AI配置
- ✅ 多AI模型支持
- ✅ 定时任务系统
- ✅ 个性化AI洞察

### AI功能更新历史
- **v1.0.0**: 
  - 🤖 集成OpenRouter AI API
  - ⚙️ Web界面AI配置功能
  - 🔄 自动定时任务系统
  - 🎯 多模型选择支持
  - 🔒 安全的本地配置存储
  - 🧪 完善的测试和调试工具

### 开发计划
- [ ] 移动端适配和响应式优化
- [ ] 计划提醒和通知功能
- [ ] 数据统计和可视化图表
- [ ] 计划模板和快速录入
- [ ] 云端同步和多设备支持
- [ ] 插件系统和功能扩展
- [ ] 更多主题和界面个性化
- [ ] 团队协作和分享功能
- [ ] AI功能增强计划：
  - [ ] 更多AI服务提供商支持
  - [ ] AI使用统计和监控
  - [ ] 智能计划推荐
  - [ ] 语音输入和AI对话
  - [ ] AI数据分析和趋势预测

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
# 确保安装了所有依赖
pip install -r requirements.txt
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

**Q: AI功能无法使用**
```bash
# 方式A: 通过Web界面配置（推荐）
python web_server.py
# 访问 http://localhost:8000，点击"⚙️ 设置"配置AI功能

# 方式B: 检查配置文件
ls settings.xml              # 检查配置文件是否存在
cat settings.xml             # 查看配置内容

# 方式C: 检查API密钥
python -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('settings.xml')
    ai_elem = tree.find('ai')
    if ai_elem is not None and ai_elem.find('openrouterApiKey') is not None:
        print('API密钥已配置')
    else:
        print('API密钥未配置')
except:
    print('配置文件不存在或格式错误')
"

# 方式D: 测试AI功能
python tests/test_weekly_task.py   # 运行AI功能测试
python tests/test_ai_config.py     # 测试配置读取
```

**Q: 定时任务不执行**
```bash
# 检查AI功能是否启用
python -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('settings.xml')
    ai_elem = tree.find('ai')
    enabled = ai_elem.find('enabled')
    if enabled is not None and enabled.text == 'true':
        print('AI功能已启用')
    else:
        print('AI功能未启用，请在设置中开启')
except:
    print('请先配置AI功能')
"

# 检查schedule库
pip list | grep schedule || pip install schedule

# 手动测试定时任务
python tests/test_weekly_task.py

# 查看定时任务状态
python -c "from weekly_task import WeeklyTaskManager; mgr = WeeklyTaskManager(); print('定时任务初始化成功' if mgr else '初始化失败')"
```

**Q: Web界面AI设置不保存**
```bash
# 检查文件写入权限
touch settings.xml && echo "权限正常" || echo "权限不足"

# 检查Web服务器日志
python web_server.py
# 在浏览器中操作设置，观察终端输出

# 手动验证保存功能
python -c "
from weekly_task import WeeklyTaskManager
mgr = WeeklyTaskManager()
print('当前配置读取正常' if mgr else '配置读取失败')
"
```

**Q: 数据保存失败**
- 检查保存路径是否存在且可写
- 确认磁盘空间充足
- 查看设置面板中的保存路径配置

### 技术支持
- **问题反馈**: 通过GitHub Issues报告问题
- **功能建议**: 通过Discussions讨论新功能
- **文档问题**: 通过Pull Request改进文档
- **AI功能支持**: 查看OpenRouter API文档获取更多信息
- **详细文档**: 更多AI功能的详细说明可在`docs/archived/`目录中找到原始文档
- **测试指南**: 测试脚本使用说明请参考`tests/README.md`

### 获取帮助
```bash
# 查看帮助信息
python launcher.py --help
python main_launcher.py --help

# AI功能相关测试
python tests/test_weekly_task.py          # 测试AI定时任务
python tests/test_ai_config.py            # 测试AI配置读取
python tests/demo_ai_config.py            # AI功能演示
python tests/test_model_config.py         # 测试模型配置

# 快速诊断
python -c "
import sys
print(f'Python版本: {sys.version}')

try:
    import tkinter
    print('✓ GUI组件可用')
except ImportError:
    print('✗ GUI组件不可用')

try:
    import json
    print('✓ JSON支持可用')
except ImportError:
    print('✗ JSON支持不可用')

try:
    import xml.etree.ElementTree
    print('✓ XML解析可用')
except ImportError:
    print('✗ XML解析不可用')

try:
    import schedule
    print('✓ 定时任务库可用')
except ImportError:
    print('✗ 定时任务库不可用，运行: pip install schedule')

try:
    import openai
    print('✓ OpenAI库可用')
except ImportError:
    print('✗ OpenAI库不可用，运行: pip install openai')
"

# Web服务状态检查
python -c "
import socket
def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

if check_port('localhost', 8000):
    print('✓ Web服务正在运行 (端口8000)')
else:
    print('✗ Web服务未运行，执行: python web_server.py')
"
```

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
