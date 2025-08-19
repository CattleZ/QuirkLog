# QuirkLog - 每日计划与总结应用程序

一个现代化的每日计划与总结应用程序，基于Web技术构建，集成AI智能助手，支持跨平台运行，帮助您更好地管理时间、记录生活、进行自我反思和提升个人效率。

## 🌟 项目特色

QuirkLog 是一个纯Web版的个人时间管理和生活记录工具，专注于提供现代化的浏览器体验。通过集成AI智能助手，为用户提供个性化的成长建议和自我反思洞察。

### ⭐ 核心亮点
- **🌐 纯Web体验**: 基于现代Web技术，无需安装客户端，浏览器即可使用
- **🤖 AI智能助手**: 集成OpenRouter AI，提供每周个性化洞察和成长建议
- **📱 响应式设计**: 完美适配桌面、平板和移动设备
- **🔄 自动定时任务**: 后台智能运行，定期生成AI分析报告
- **💾 本地数据存储**: 隐私安全，数据完全本地化管理
- **🚀 一键启动**: 智能启动器，自动启动Web服务和定时任务

## 🎯 核心功能

### 📅 智能计划管理
- **多维度分类**: 支持重要性、紧急度双重分类，基于艾森豪威尔矩阵
- **时间规划**: 精确的开始时间和计划时长设定
- **实时状态跟踪**: 一键标记完成状态，可视化进度管理
- **批量操作**: 高效的计划批量编辑和管理功能

### 📝 深度反思总结
- **完成率分析**: 自动统计并生成可视化完成情况图表
- **成长记录**: 记录每日进步点和个人改进建议
- **感恩日记**: 记录生活中的感动瞬间和感恩时刻
- **Markdown支持**: 支持富文本格式的深度思考记录
- **问题分析**: 帮助识别和分析未完成任务的原因

### 🤖 AI智能洞察
- **每周AI总结**: 基于您的计划和总结数据，AI自动生成个性化洞察
- **定时任务系统**: 每周一上午10点自动执行AI分析
- **多模型支持**: 支持多种AI模型，包括免费和付费选项
- **Web界面配置**: 可视化配置AI功能，无需手动编辑配置文件
- **隐私保护**: API密钥本地存储，AI分析结果本地保存

### 💾 智能数据管理
- **JSON格式存储**: 开放的数据格式，易于备份和迁移
- **自动保存机制**: 智能防丢失，确保数据安全
- **历史记录浏览**: 按日期组织的完整历史数据
- **自定义存储路径**: 灵活的数据保存位置配置
- **多种文件命名格式**: 支持个性化的文件命名规则

## 💻 技术架构

### 前端技术栈
- **HTML5 + CSS3**: 现代化语义标记，响应式布局设计
- **原生JavaScript (ES6+)**: 模块化开发，异步数据处理
- **Flexbox/Grid**: 灵活的响应式布局系统
- **现代UI设计**: 简洁直观的用户界面，优秀的用户体验

### 后端架构
- **Python 3.6+**: 核心开发语言，稳定可靠
- **HTTP Server**: 基于Python标准库的轻量级Web服务器
- **零外部依赖**: 核心功能无需额外服务，即开即用

### AI集成
- **OpenRouter API**: 支持多种主流AI模型
- **本地配置管理**: 安全的API密钥存储
- **智能调度系统**: 基于schedule库的定时任务
- **错误处理机制**: 完善的异常处理和重试逻辑

### 数据管理
- **JSON数据格式**: 轻量级、可读性强的数据存储
- **XML配置管理**: 结构化的应用配置文件
- **本地文件系统**: 完全本地化的数据持久化

## 🚀 快速开始

### 方式一：源代码运行（推荐开发者）

```bash
# 1. 克隆项目
git clone https://github.com/CattleZ/QuirkLog.git
cd QuirkLog

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 启动应用程序
python launcher.py          # 🌟 推荐：智能启动器
# 或者
python main_launcher.py     # 带菜单的启动器
# 或者
python web_server.py        # 直接启动Web服务器

# 4. 打开浏览器
# 应用会自动打开浏览器，或手动访问 http://localhost:8000
```

### 方式二：预编译版本（推荐普通用户）

```bash
# 1. 下载对应平台的发布包
# 从 GitHub Releases 下载 QuirkLog-v1.0.0-*.zip

# 2. 解压并运行
unzip QuirkLog-v1.0.0-*.zip
cd QuirkLog

# 3. 双击运行
# Windows: QuirkLog.exe
# macOS/Linux: ./QuirkLog

# 4. 浏览器自动打开或手动访问 http://localhost:8000
```

### 方式三：一键构建（开发者）

```bash
# 构建跨平台可执行文件
python build_scripts/auto_build.py

# 生成的文件在 dist/ 目录中
# 包含完整的安装包和启动脚本
```

## 📖 使用指南

### 🎯 基本使用流程

1. **🚀 启动应用**
   - 运行 `python launcher.py` 或双击可执行文件
   - 浏览器自动打开并访问 http://localhost:8000
   - 定时任务自动在后台启动

2. **📝 制定每日计划**
   - 点击"📅 今日计划"标签
   - 添加计划描述、设置重要性和紧急度
   - 指定开始时间和预计时长

3. **✅ 跟踪执行进度**
   - 在计划列表中实时标记完成状态
   - 查看可视化的完成进度统计

4. **🤔 记录反思总结**
   - 切换到"📝 今日总结反思"标签
   - 记录今日进步、感恩时刻和深度思考
   - 分析未完成任务的原因

5. **💾 数据自动保存**
   - 系统自动保存所有数据到本地
   - 支持自定义保存路径和文件命名格式

### ⚙️ AI功能配置

#### 快速配置步骤

1. **获取API密钥**
   ```bash
   # 访问 https://openrouter.ai/
   # 注册免费账户并创建API密钥
   ```

2. **在应用中配置**
   - 点击页面右上角的 "⚙️ 设置" 按钮
   - 找到 "🤖 AI智能助手设置" 区域
   - 开启 "启用AI功能" 开关
   - 输入您的 OpenRouter API 密钥
   - 选择合适的AI模型（默认免费模型已预选）
   - 点击 "🧪 测试AI连接" 验证配置
   - 点击 "💾 保存设置" 完成配置

3. **自动定时任务**
   - 配置成功后，系统每周一上午10:00自动生成AI洞察
   - AI分析您的计划执行情况和成长轨迹
   - 生成的洞察报告保存在 `weekly_insights/` 目录

#### 支持的AI模型

| 模型 | 类型 | 特点 | 推荐使用场景 |
|------|------|------|-------------|
| deepseek/deepseek-r1-0528-qwen3-8b:free | 免费 | 中文友好，日常使用 | 🌟 默认推荐 |
| openai/gpt-3.5-turbo | 付费 | 高质量对话 | 深度分析 |
| openai/gpt-4o-mini | 付费 | 强推理能力 | 复杂问题 |
| anthropic/claude-3-haiku | 付费 | 长文本处理 | 详细总结 |
| meta-llama/llama-3.1-8b-instruct:free | 免费 | 开源替代 | 隐私优先 |

### 🛠️ 高级功能

- **📊 历史数据浏览**: 通过侧边栏浏览往期记录
- **🎨 个性化设置**: 自定义文件命名格式和保存路径  
- **🔄 批量操作**: 支持计划的批量编辑和管理
- **📱 响应式体验**: 完美适配手机、平板和桌面设备

## 🏗️ 项目结构

### � 核心文件组织

```
QuirkLog/
├── 🚀 launcher.py              # 智能启动器（推荐入口）
├── 📋 main_launcher.py         # 带菜单的启动器
├── 🌐 web_server.py           # Web服务器核心
├── 🤖 weekly_task.py          # AI定时任务系统
├── ⚙️ config_template.py      # 配置文件模板
├── 🌍 index.html              # 主Web界面
├── 🎨 style.css               # 样式文件
├── ⚡ script.js               # 前端交互逻辑
├── 📄 weekly_summary_template.md # AI分析模板
├── 🔧 settings.xml            # 用户配置文件
├── � requirements.txt        # Python依赖
└── 📚 README.md               # 项目文档
```

### 🧪 测试与开发

```
tests/                          # 测试脚本集合
├── 📋 README.md               # 测试说明文档
├── 🔬 test_ai_config.py       # AI配置功能测试
├── ⏰ test_weekly_task.py     # 定时任务测试
├── 🎯 test_model_config.py    # AI模型配置测试
└── 🎪 demo_ai_config.py       # AI功能演示脚本
```

### 🔨 构建与部署

```
build_scripts/                  # 构建工具集
├── 📖 README.md               # 构建说明文档
├── 🚀 auto_build.py           # 一键自动构建（推荐）
├── 🔧 build_package.py        # 高级打包工具
├── 📦 package.py              # 简单打包脚本
└── 🧠 smart_launcher.py       # 智能启动器
```

### 📊 AI功能相关

```
📁 weekly_insights/             # AI生成洞察存储目录
    └── weekly_insight_YYYY-MM-DD.json   # 按日期保存的AI分析报告

🤖 AI工作流程:
1. 数据收集 → 分析用户的计划和总结数据
2. AI处理 → 调用OpenRouter API生成洞察
3. 结果保存 → 本地保存个性化分析报告
4. 定时执行 → 每周一上午10:00自动运行
```

## 🔧 开发者指南

### 🛠️ 开发环境搭建

```bash
# 1. 克隆项目
git clone https://github.com/CattleZ/QuirkLog.git
cd QuirkLog

# 2. 设置Python虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 3. 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-build.txt

# 4. 配置AI功能（开发测试）
python web_server.py
# 在浏览器中访问 http://localhost:8000 进行配置

# 5. 运行测试
python tests/test_ai_config.py      # 测试AI配置
python tests/test_weekly_task.py    # 测试定时任务
python tests/demo_ai_config.py      # 运行功能演示
```

### 🧪 测试与验证

| 测试脚本 | 功能说明 | 用途 |
|----------|----------|------|
| `test_ai_config.py` | AI配置系统测试 | 验证XML配置读取和API设置 |
| `test_weekly_task.py` | 定时任务功能测试 | 测试AI任务调度和执行 |
| `test_model_config.py` | AI模型配置测试 | 验证多模型支持和切换 |
| `demo_ai_config.py` | 完整功能演示 | 交互式体验所有AI功能 |

```bash
# 运行单个测试
python tests/test_ai_config.py

# 批量运行所有测试
for test in tests/test_*.py; do python "$test"; done

# 运行演示程序（推荐新用户）
python tests/demo_ai_config.py
```

### 📦 构建与打包

```bash
# 🌟 推荐：一键自动构建
python build_scripts/auto_build.py

# 构建结果在 dist/ 目录：
# ├── QuirkLog(.exe)           # 可执行文件
# ├── install.sh/.bat          # 安装脚本
# ├── README.md               # 使用说明
# └── 所有必需的资源文件

# 高级自定义构建
python build_scripts/build_package.py  # 可配置构建选项
python build_scripts/package.py        # 简单快速构建
```

### 🎯 代码规范
- 遵循 **PEP 8** Python代码规范
- 使用**中文注释**增强可读性
- **模块化设计**，功能清晰分离
- **Web优先**，响应式设计理念
- **AI功能模块化**，易于扩展和维护

## 📊 版本信息

### 🚀 当前版本：v1.0.0

#### ✨ 核心功能特性
- ✅ **完整的计划管理系统** - 多维度分类，状态跟踪
- ✅ **深度反思总结模块** - 成长记录，感恩日记  
- ✅ **现代化Web界面** - 响应式设计，跨设备兼容
- ✅ **自动化构建部署** - 一键打包，跨平台支持
- ✅ **多格式数据管理** - JSON存储，自定义路径

#### 🤖 AI智能助手功能
- ✅ **OpenRouter AI集成** - 多模型支持，免费可用
- ✅ **Web界面AI配置** - 可视化设置，一键测试
- ✅ **智能定时任务** - 每周自动生成AI洞察
- ✅ **个性化分析报告** - 基于用户数据的成长建议
- ✅ **安全隐私保护** - 本地存储，数据不外传

#### 🔧 技术架构升级  
- ✅ **纯Web架构** - 移除GUI依赖，专注Web体验
- ✅ **智能启动器** - 自动启动Web服务和定时任务
- ✅ **模块化设计** - 清晰的代码结构，易于维护
- ✅ **完善测试覆盖** - 全面的功能测试和演示脚本

### 🎯 开发规划

#### 📱 即将到来的功能
- [ ] **移动端优化** - 原生移动应用体验
- [ ] **智能提醒系统** - 计划提醒和通知功能  
- [ ] **数据可视化** - 图表统计和趋势分析
- [ ] **计划模板库** - 预设模板和快速创建
- [ ] **多主题支持** - 个性化界面主题

#### 🤖 AI功能增强计划
- [ ] **多AI提供商支持** - 集成Google AI、Anthropic Claude
- [ ] **AI使用分析** - 使用统计和监控面板
- [ ] **智能计划推荐** - AI驱动的计划优化建议
- [ ] **语音交互界面** - 语音输入和AI对话
- [ ] **月度年度报告** - 长期趋势分析和洞察

#### 🌟 高级功能规划
- [ ] **云端同步** - 多设备数据同步
- [ ] **团队协作** - 计划分享和协作功能
- [ ] **插件生态** - 第三方插件系统
- [ ] **API开放平台** - 开发者API接口
- [ ] **企业版功能** - 团队管理和高级分析

## 🛠️ 故障排除

### 🚨 常见问题解决

#### **Q: 应用启动失败**
```bash
# 1. 检查Python环境
python --version  # 需要 Python 3.6+

# 2. 重新安装依赖
pip install -r requirements.txt

# 3. 检查当前目录
pwd  # 确保在QuirkLog项目根目录

# 4. 重新启动
python launcher.py
```

#### **Q: Web服务无法访问**
```bash
# 检查端口占用情况
python -c "
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 8000))
sock.close()
print('端口8000已被占用' if result == 0 else '端口8000可用')
"

# 尝试其他端口
python web_server.py --port 8080
```

#### **Q: AI功能无法使用**
```bash
# 🌟 推荐：通过Web界面配置
python launcher.py
# 在浏览器中点击"⚙️ 设置" -> "AI智能助手设置"

# 检查配置文件
ls settings.xml && echo "配置文件存在" || echo "配置文件缺失"

# 验证API密钥格式
python -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('settings.xml')
    ai_elem = tree.find('ai')
    api_key = ai_elem.find('openrouterApiKey')
    if api_key is not None and api_key.text:
        print('✅ API密钥已配置')
        print(f'格式检查: {\"正确\" if api_key.text.startswith(\"sk-or-v1-\") else \"错误\"}')
    else:
        print('❌ API密钥未配置')
except Exception as e:
    print(f'❌ 配置文件读取失败: {e}')
"

# 测试AI连接
python tests/test_ai_config.py
```

#### **Q: 定时任务不工作**
```bash
# 检查AI功能状态
python -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('settings.xml')
    ai_elem = tree.find('ai')
    enabled = ai_elem.find('enabled')
    print(f'AI功能状态: {\"已启用\" if enabled.text == \"true\" else \"已禁用\"}')
except:
    print('请先配置AI功能')
"

# 手动测试定时任务
python tests/test_weekly_task.py

# 立即执行一次AI任务
python -c "from weekly_task import WeeklyTaskManager; WeeklyTaskManager().run_task_now()"
```

### 🔧 系统诊断工具

```bash
# 🩺 系统健康检查
python -c "
import sys
print(f'🐍 Python版本: {sys.version}')

# 检查核心依赖
modules = [
    ('json', 'JSON处理'),
    ('xml.etree.ElementTree', 'XML解析'),
    ('http.server', 'Web服务器'),
    ('webbrowser', '浏览器控制')
]

for module, desc in modules:
    try:
        __import__(module)
        print(f'✅ {desc}: 可用')
    except ImportError:
        print(f'❌ {desc}: 不可用')

# 检查AI相关依赖
ai_modules = [
    ('schedule', '定时任务'),
    ('openai', 'AI接口')
]

for module, desc in ai_modules:
    try:
        __import__(module)
        print(f'✅ {desc}: 可用')
    except ImportError:
        print(f'⚠️  {desc}: 不可用 (pip install {module})')
"

# 🌐 Web服务状态检查
python -c "
import socket
def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

ports = [8000, 8080, 3000]
for port in ports:
    status = '🟢 运行中' if check_port(port) else '🔴 空闲'
    print(f'端口 {port}: {status}')
"
```

### 📞 获取帮助

#### 🎯 官方资源
- **📚 项目文档**: [GitHub README](https://github.com/CattleZ/QuirkLog)
- **🐛 问题反馈**: [GitHub Issues](https://github.com/CattleZ/QuirkLog/issues)
- **💡 功能建议**: [GitHub Discussions](https://github.com/CattleZ/QuirkLog/discussions)
- **🔗 OpenRouter API**: [官方文档](https://openrouter.ai/docs)

#### 🧪 测试和演示脚本
```bash
# AI功能完整演示（推荐新用户）
python tests/demo_ai_config.py

# 分模块测试
python tests/test_ai_config.py       # AI配置测试
python tests/test_weekly_task.py     # 定时任务测试
python tests/test_model_config.py    # 模型配置测试

# 查看启动器帮助
python launcher.py --help
python main_launcher.py  # 交互式菜单
```

## 📄 许可证与致谢

### 📜 开源许可
本项目采用 **MIT 许可证**，详情请查看 [LICENSE](LICENSE) 文件。

### 🙏 技术致谢
- **Python软件基金会** - 提供优秀的Python语言和生态
- **OpenRouter** - 提供便捷的AI模型接口服务
- **现代Web标准** - HTML5、CSS3、ES6+技术支持
- **PyInstaller** - 跨平台应用打包工具
- **开源社区** - 无数开发者的贡献和支持

### 👥 贡献者
感谢所有为QuirkLog项目贡献代码、文档、测试和建议的开发者们！

#### 🤝 如何贡献
1. **Fork** 项目仓库
2. **创建特性分支**: `git checkout -b feature/AmazingFeature`
3. **提交更改**: `git commit -m 'Add some AmazingFeature'`
4. **推送分支**: `git push origin feature/AmazingFeature`
5. **创建 Pull Request**

---

<div align="center">

### 🌟 QuirkLog - 让每一天都有记录，让每一次反思都有价值 ✨

**现代化 · 智能化 · 个性化的每日计划与总结应用**

[![GitHub stars](https://img.shields.io/github/stars/CattleZ/QuirkLog?style=social)](https://github.com/CattleZ/QuirkLog)
[![GitHub forks](https://img.shields.io/github/forks/CattleZ/QuirkLog?style=social)](https://github.com/CattleZ/QuirkLog/fork)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>
