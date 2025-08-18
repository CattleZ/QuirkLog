# 贡献指南

感谢您对 QuirkLog 项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题
- 在提交问题之前，请先搜索是否已有相关的issue
- 请使用清晰的标题和详细的描述
- 如果可能，请提供重现步骤

### 提交代码
1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 开发环境设置

### 环境要求
- Python 3.7+
- tkinter (通常随Python一起安装)

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行项目
```bash
# GUI版本
python daily_planner.py

# CLI版本  
python daily_planner_cli.py

# Web版本
python web_server.py
```

## 代码规范

- 遵循 PEP 8 Python 代码规范
- 使用有意义的变量名和函数名
- 添加适当的注释
- 为新功能编写测试

## 提交信息格式

请使用以下格式：
```
类型: 简短描述

详细描述（可选）
```

类型示例：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 添加测试

感谢您的贡献！ 🎉
