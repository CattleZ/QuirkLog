# 🚀 QuirkLog AI配置快速指南

## 一分钟快速配置AI功能

### 步骤1: 启动应用
```bash
cd QuirkLog
python web_server.py
```

### 步骤2: 配置AI
1. 在浏览器中打开 http://localhost:8000
2. 点击右上角 "⚙️ 设置" 按钮
3. 找到 "🤖 AI智能助手设置" 区域

### 步骤3: 获取API密钥
1. 访问 https://openrouter.ai/
2. 注册免费账户
3. 在控制台创建API密钥

### 步骤4: 完成配置
1. 启用 "启用AI功能" 开关
2. 输入API密钥到 "OpenRouter API密钥" 字段
3. 点击 "🧪 测试AI连接" 验证
4. 点击 "💾 保存设置"

### 步骤5: 开始使用
```bash
# 启动AI功能
python main_launcher.py
```

## 🎯 功能验证

配置完成后，您可以：
- ✅ 每周六上午9点自动获取AI洞察
- ✅ 每周日晚上7点获取周末反思
- ✅ 随时手动执行 `python weekly_task.py`

## ⚡ 故障排除

**问题**: 测试连接失败
**解决**: 检查API密钥是否正确粘贴

**问题**: 定时任务不工作  
**解决**: 确保AI功能已启用且API密钥有效

**问题**: 缺少依赖
**解决**: 运行 `pip install -r requirements.txt`

---
🎉 **恭喜！您已成功配置AI智能助手功能！**
