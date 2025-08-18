# 测试与演示脚本目录

本目录包含QuirkLog项目的所有测试脚本和演示程序，用于验证功能正常性和展示项目特性。

## 📋 文件说明

| 文件名 | 用途 | 说明 |
|--------|------|------|
| `test_ai_config.py` | AI配置测试 | 测试AI配置读取、XML解析和设置验证 |
| `test_weekly_task.py` | AI定时任务测试 | 测试AI定时任务功能和API连接 |
| `test_model_config.py` | AI模型配置测试 | 测试多AI模型配置和切换功能 |
| `demo_ai_config.py` | AI功能演示 | 完整的AI配置功能演示程序 |

## 🚀 使用方法

### 运行单个测试

```bash
# 从项目根目录运行（推荐）
cd QuirkLog

# 测试AI配置功能
python tests/test_ai_config.py

# 测试AI定时任务
python tests/test_weekly_task.py

# 测试AI模型配置
python tests/test_model_config.py

# 运行AI功能演示
python tests/demo_ai_config.py
```

### 批量运行测试

```bash
# 运行所有测试脚本
for test in tests/test_*.py; do
    echo "运行测试: $test"
    python "$test"
    echo "---"
done

# 或者使用一行命令
python -c "
import subprocess
import glob
import os

# 确保在项目根目录
if not os.path.exists('weekly_task.py'):
    print('请在QuirkLog项目根目录运行此命令')
    exit(1)

for test_file in sorted(glob.glob('tests/test_*.py')):
    print(f'\\n=== 运行测试: {test_file} ===')
    result = subprocess.run(['python', test_file], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print('错误:', result.stderr)
    print('='*50)
"
```

## 🧪 测试内容说明

### AI配置测试 (`test_ai_config.py`)
- ✅ 测试XML配置文件读取
- ✅ 验证AI功能启用状态
- ✅ 检查API密钥配置
- ✅ 测试配置优先级机制
- ✅ 验证错误处理

### AI定时任务测试 (`test_weekly_task.py`)
- ✅ 测试WeeklyTaskManager初始化
- ✅ 验证API连接功能
- ✅ 测试定时任务执行
- ✅ 检查AI洞察生成
- ✅ 验证数据保存机制

### AI模型配置测试 (`test_model_config.py`)
- ✅ 测试多种AI模型配置
- ✅ 验证模型切换功能
- ✅ 检查模型参数传递
- ✅ 测试自定义模型设置
- ✅ 验证模型配置优先级

### AI功能演示 (`demo_ai_config.py`)
- 🎯 完整的功能演示流程
- 🎯 交互式配置展示
- 🎯 实时功能验证
- 🎯 用户界面模拟
- 🎯 错误处理演示

## 📊 测试覆盖范围

### 功能测试
- [x] AI配置系统
- [x] 定时任务机制
- [x] API连接验证
- [x] 数据存储管理
- [x] 错误处理机制
- [x] 多模型支持

### 集成测试
- [x] Web界面与后端集成
- [x] XML配置文件处理
- [x] OpenRouter API集成
- [x] 定时任务调度
- [x] 数据持久化

### 性能测试
- [x] API响应时间
- [x] 配置加载速度
- [x] 数据保存性能
- [x] 内存使用情况

## ⚠️ 注意事项

### 运行要求
- 确保已安装所有依赖：`pip install -r requirements.txt`
- 部分测试需要有效的OpenRouter API密钥
- 建议在项目根目录运行测试脚本

### API密钥配置
```bash
# 方式1: 通过Web界面配置（推荐）
python web_server.py
# 访问 http://localhost:8000，在设置中配置API密钥

# 方式2: 环境变量配置
export OPENROUTER_API_KEY="sk-or-v1-your-api-key"

# 方式3: 配置文件
cp config_template.py config.py
# 编辑config.py添加API密钥
```

### 测试环境
- **开发环境**: 完整功能测试，包括API调用
- **CI/CD环境**: 跳过需要API密钥的测试
- **离线环境**: 仅运行不需要网络的测试

## 🐛 故障排除

### 常见问题

**Q: 测试提示"缺少依赖"**
```bash
pip install -r requirements.txt
```

**Q: API连接测试失败**
```bash
# 检查API密钥配置
python -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('settings.xml')
    ai_elem = tree.find('ai')
    if ai_elem is not None:
        print('配置文件存在')
        api_key = ai_elem.find('openrouterApiKey')
        if api_key is not None and api_key.text:
            print('API密钥已配置')
        else:
            print('API密钥未配置')
    else:
        print('AI配置不存在')
except FileNotFoundError:
    print('配置文件不存在，请先配置AI功能')
"
```

**Q: 测试脚本找不到模块**
```bash
# 确保在项目根目录运行
cd QuirkLog

# 检查项目结构
ls -la weekly_task.py  # 应该存在此文件

# 运行测试
python tests/test_ai_config.py

# 如果仍有问题，检查Python路径
python -c "
import sys
from pathlib import Path
print('当前工作目录:', Path.cwd())
print('Python路径:', sys.path[:3])
"
```

### 调试模式
```bash
# 启用详细输出
python -v tests/test_ai_config.py

# 使用调试器
python -m pdb tests/test_ai_config.py
```

## 📚 参考文档

- [主项目README](../README.md) - 项目总体说明
- [AI配置指南](../docs/archived/) - 详细的AI功能文档
- [OpenRouter API文档](https://openrouter.ai/docs) - API使用说明

---

*这些测试脚本帮助确保QuirkLog的AI功能稳定可靠，持续为用户提供优质的智能助手体验！*
