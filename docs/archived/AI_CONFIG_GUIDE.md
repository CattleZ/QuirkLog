# 🤖 AI智能助手配置指南

## 概述
QuirkLog现在支持AI智能助手功能，通过OpenRouter API提供每周洞察和个性化建议。本指南将帮助您完成AI功能的配置。

## 🔧 配置步骤

### 1. 获取OpenRouter API密钥

1. **访问OpenRouter网站**: https://openrouter.ai/
2. **注册账户**: 使用邮箱注册一个免费账户
3. **获取API密钥**: 
   - 登录后进入控制台
   - 找到API Keys部分
   - 创建新的API密钥
   - 复制密钥（格式类似：`sk-or-v1-xxxxxxxxxxxxxxxx`）

### 2. 在QuirkLog中配置AI功能

1. **打开设置面板**: 点击右上角的"⚙️ 设置"按钮
2. **找到AI智能助手设置**区域
3. **启用AI功能**: 打开"启用AI功能"开关
4. **输入API密钥**: 将获取的API密钥粘贴到"OpenRouter API密钥"字段
5. **确认服务地址**: 通常保持默认的`https://openrouter.ai/api/v1`
6. **测试连接**: 点击"🧪 测试AI连接"按钮验证配置是否正确
7. **保存设置**: 点击"💾 保存设置"按钮

### 3. 验证配置

配置成功后，您的设置将保存在`settings.xml`文件中，格式如下：

```xml
<ai>
    <enabled>true</enabled>
    <openrouterApiKey>sk-or-v1-your-api-key-here</openrouterApiKey>
    <openrouterBaseUrl>https://openrouter.ai/api/v1</openrouterBaseUrl>
</ai>
```

## 🚀 使用AI功能

### 每周定时任务

配置完成后，您可以使用以下方式启动AI每周洞察：

```bash
# 方式1: 使用主启动器（推荐）
python main_launcher.py

# 方式2: 直接运行每周任务
python weekly_task.py

# 方式3: 测试AI功能
python test_weekly_task.py
```

### 功能特性

- **🔄 自动执行**: 每周六上午9点和周日晚上7点自动运行
- **🤖 AI洞察**: 使用深度学习模型生成个性化建议
- **💾 数据保存**: AI生成的洞察自动保存到`weekly_insights/`目录
- **🧪 测试模式**: 支持立即执行任务进行测试

## 🛠 故障排除

### 常见问题

**Q: API连接测试失败**
- 检查API密钥是否正确
- 确认网络连接正常
- 验证OpenRouter账户是否有效

**Q: 提示"未安装openai库"**
```bash
pip install openai schedule
```

**Q: 定时任务不执行**
- 确保AI功能已启用
- 检查API密钥配置
- 运行测试模式验证功能

**Q: 找不到设置文件**
- 设置会自动保存到`settings.xml`
- 如果文件丢失，重新配置即可

### 调试命令

```bash
# 检查AI配置
python test_ai_config.py

# 测试API连接
python -c "from weekly_task import WeeklyTaskManager; mgr = WeeklyTaskManager(); mgr.run_task_now()"

# 查看设置文件
cat settings.xml
```

## 📋 API使用说明

### 支持的模型
- 默认使用: `deepseek/deepseek-r1-0528-qwen3-8b:free`
- 免费模型，无需付费
- 支持中文对话

### 请求限制
- 每月免费额度有限
- 建议合理使用，避免频繁测试
- 可在OpenRouter控制台查看使用情况

## 🔒 隐私与安全

- **本地存储**: API密钥和设置仅保存在本地
- **安全传输**: 所有API请求使用HTTPS加密
- **数据隐私**: AI洞察仅保存在本地文件中
- **可选功能**: 随时可以禁用AI功能

## 📞 技术支持

如需帮助，请：
1. 查看项目README文档
2. 检查GitHub Issues
3. 运行测试脚本诊断问题

---

*配置完成后，您就可以享受AI助手带来的每周个人成长洞察了！🎉*
